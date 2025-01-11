from flask import Blueprint, jsonify, request, render_template, current_app
from app.extensions import db
from app.models import Player, WeeklyGame, PlayerGameSignup
from app.utils.validators import validate_email_format, validate_phone_format
from app.templates.emails import EMAIL_TEMPLATES
from datetime import datetime
import threading, requests
from app.utils.whatsapp_notifications import WhatsAppNotifier
from flask_login import login_required, current_user


main = Blueprint('main', __name__)

def get_current_game(game_id):
    current_game = WeeklyGame.query.filter(
        WeeklyGame.id == game_id
    ).first()
    
    return current_game

def send_signup_notifications(app, player, game):
    with app.app_context():
        try:
            # Format game details
            game_date = game.date.strftime('%A, %B %d, %Y')
            game_start = game.start_time.strftime('%I:%M %p')
            game_end = game.end_time.strftime('%I:%M %p')
            
            # Get player position
            player_position = PlayerGameSignup.query.filter_by(
                game_id=game.id,
                is_cancelled=False
            ).count()
            
            player_signups = PlayerGameSignup.query.filter_by(
                    player_id=player.id,
                    game_id=game.id,
                )
            
            signup = max(player_signups, key=lambda x: x.signup_time)
            
            # Send sign up notification
            if signup.is_cancelled == False:
                # Queue confirmation email to player
                app.email_queue.add_to_queue(
                    'signup_confirmation',
                    player.email,
                    player_name=player.name,
                    game_date=game_date,
                    game_start_time=game_start,
                    game_end_time=game_end,
                    game_location=game.location,
                    position=player_position,
                    max_players=game.max_players
                )
            
                # Add WhatsApp notification
                if app.config['WHATSAPP_ENABLED'] and player.phone:
                    whatsapp = WhatsAppNotifier(app,app.config['WHATSAPP_PHONE_ID'],app.config['WHATSAPP_TOKEN'])
                    game_date = game.date.strftime('%A, %B %d, %Y')
                    game_time = f"{game.start_time.strftime('%I:%M %p')} - {game.end_time.strftime('%I:%M %p')}"
                    
                    message = whatsapp.format_signup_message(
                        player.name,
                        game_date,
                        game_time,
                        game.location
                    )
                
                    # Convert phone to international format (assuming Turkish numbers)
                    phone_digits = ''.join(filter(str.isdigit, player.phone))
                    if phone_digits.startswith('5'):
                        phone_digits = '90' + phone_digits
                    
                    # In test mode, send template message
                    whatsapp.send_message(
                        phone_digits, 
                        message,  # message not needed for template
                        use_template=True  # This will use the hello_world template
                    )
            
                # Queue update email to organizers
                player_list = get_player_list(game.id)
                for organizer in app.config['ORGANIZERS']:
                    app.email_queue.add_to_queue(
                        'organizer_update',
                        organizer,
                        game_date=game_date,
                        player_list=player_list,
                        player_count=player_position,
                        max_players=app.config['MAX_PLAYERS'],
                        recent_change=f"Added: {player.name}"
                    )
            
            # Send cancellation notification
            elif signup.is_cancelled == True:
                app.email_queue.add_to_queue(
                'cancellation_confirmation',
                player.email,
                player_name=player.name,
                game_date=game.date.strftime('%A, %B %d, %Y')
                )

                # Add WhatsApp notification
                if app.config['WHATSAPP_ENABLED'] and player.phone:
                    whatsapp = WhatsAppNotifier(app,app.config['WHATSAPP_PHONE_ID'],app.config['WHATSAPP_TOKEN'])
                    game_date = game.date.strftime('%A, %B %d, %Y')
                    game_time = f"{game.start_time.strftime('%I:%M %p')} - {game.end_time.strftime('%I:%M %p')}"
                    
                    message = whatsapp.format_cancellation_message(
                        player.name,
                        game_date,
                    )
                    
                    # Convert phone to international format (assuming Turkish numbers)
                    phone_digits = ''.join(filter(str.isdigit, player.phone))
                    if phone_digits.startswith('5'):
                        phone_digits = '90' + phone_digits
                    
                    # In test mode until whatsapp business phone added
                    whatsapp.send_message(
                        phone_digits, 
                        message,
                        use_template=True  # This will use the hello_world template
                    )
                
                # Queue update email to organizers
                player_list = get_player_list(game.id)
                for organizer in app.config['ORGANIZERS']:
                    app.email_queue.add_to_queue(
                        'organizer_update',
                        organizer,
                        game_date=game_date,
                        player_list=player_list,
                        player_count=player_position,
                        max_players=app.config['MAX_PLAYERS'],
                        recent_change=f"Removed: {player.name}"
                    )

        except Exception as e:
            current_app.logger.error(f"Error sending signup notifications: {str(e)}")

def get_player_list(game_id):
    signups = PlayerGameSignup.query.filter_by(
        game_id=game_id,
        is_cancelled=False
    ).join(Player).order_by(PlayerGameSignup.signup_time).all()
    
    return "\n".join([
        f"{i+1}. {signup.player.name}"
        for i, signup in enumerate(signups)
    ])

@main.route('/game/<int:game_id>/check_signup', methods=['GET'])
@login_required
def check_signup(game_id):
    try:
        signup = PlayerGameSignup.query.filter_by(
            player_id=current_user.id,
            game_id=game_id,
            is_cancelled=False
        ).first()
        return jsonify({"is_signed_up": bool(signup)})
    except Exception as e:
        current_app.logger.error(f"Error checking signup: {str(e)}")
        return jsonify({"error": "Failed to check signup status"}), 500

@main.route('/game/<int:game_id>/signup', methods=['POST'])
@login_required
def signup_for_game(game_id):
    try:
        game = WeeklyGame.query.get_or_404(game_id)
        
        existing_signup = PlayerGameSignup.query.filter_by(
            player_id=current_user.id,
            game_id=game_id,
            is_cancelled=False
        ).first()
        
        if existing_signup:
            return jsonify({"error": "Already signed up for this game"}), 400
            
        if game.player_count >= game.max_players:
            return jsonify({"error": "Game is full"}), 400

        signup = PlayerGameSignup(player=current_user, game=game)
        db.session.add(signup)
        game.player_count += 1
        db.session.commit()

        return jsonify({"message": "Successfully signed up for the game!"}), 201

    except Exception as e:
        current_app.logger.error(f"Error in signup: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Failed to sign up"}), 500

@main.route('/game/<int:game_id>/cancel', methods=['POST'])
@login_required
def cancel_signup(game_id):
    try:
        signup = PlayerGameSignup.query.filter_by(
            player_id=current_user.id,
            game_id=game_id,
            is_cancelled=False
        ).first()
        
        if not signup:
            return jsonify({"error": "No active signup found"}), 404

        signup.is_cancelled = True
        signup.game.player_count -= 1
        db.session.commit()

        return jsonify({"message": "Successfully cancelled signup"}), 200

    except Exception as e:
        current_app.logger.error(f"Error in cancel: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Failed to cancel signup"}), 500


@main.route('/')
def main_page():
    return render_template('main.html')

@main.route('/signup/dashboard')
@login_required
def signup_dashboard():
    return render_template('signup/dashboard.html')

@main.route('/game/<int:game_id>')
@login_required
def game_signup(game_id):
    return render_template('game.html')

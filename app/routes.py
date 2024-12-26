from flask import Blueprint, jsonify, request, render_template, current_app
from app import db
from app.models import Player, WeeklyGame, PlayerGameSignup
from app.utils.validators import validate_email_format, validate_phone_format
from app.templates.emails import EMAIL_TEMPLATES
from datetime import datetime
import threading, requests
from app.utils.whatsapp_notifications import WhatsAppNotifier



main = Blueprint('main', __name__)

def get_current_game():
    current_game = WeeklyGame.query.filter(
        WeeklyGame.date >= datetime.now().date()
    ).first()
    
    if not current_game:
        next_game_date = datetime.now().date()
        current_game = WeeklyGame(
            date=next_game_date,
            location=current_app.config['DEFAULT_LOCATION'],
            start_time=current_app.config['DEFAULT_GAME_START_TIME'],
            end_time=current_app.config['DEFAULT_GAME_END_TIME']
        )
        db.session.add(current_game)
        db.session.commit()
    
    return current_game

def send_signup_notifications(app, player, game):
    with app.app_context():
        try:
            print(app.config['WHATSAPP_TOKEN'])
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
                    max_players=app.config['MAX_PLAYERS']
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
                        recent_change=f"Removed: {player.name}"
                    )
            
            
                
        except Exception as e:
            print(f"Error sending signup notifications: {str(e)}")


def get_player_list(game_id):
    signups = PlayerGameSignup.query.filter_by(
        game_id=game_id,
        is_cancelled=False
    ).join(Player).order_by(PlayerGameSignup.signup_time).all()
    
    return "\n".join([
        f"{i+1}. {signup.player.name} ({signup.signup_time.strftime('%I:%M %p')})"
        for i, signup in enumerate(signups)
    ])

@main.route('/player-count', methods=['GET'])
def get_player_count():
    try:
        count = PlayerGameSignup.query.filter_by(
            is_cancelled=False,
            game_id=get_current_game().id
        ).count()
        return jsonify({
            "count": count,
            "max_players": current_app.config['MAX_PLAYERS']
        })
    except Exception as e:
        current_app.logger.error(f"Error getting player count: {str(e)}")
        return jsonify({"error": "Could not fetch player count"}), 500

@main.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        # Basic validation
        if not all([name, email, phone]):
            return jsonify({"error": "All fields are required!"}), 400

        # Email and phone validation
        is_valid_email, email_message = validate_email_format(email)
        if not is_valid_email:
            return jsonify({"error": f"Invalid email: {email_message}"}), 400

        is_valid_phone, phone_message = validate_phone_format(phone)
        if not is_valid_phone:
            return jsonify({"error": phone_message}), 400

        current_game = get_current_game()
        
        # Check if player exists
        existing_player = Player.query.filter(
            (Player.phone == phone) | (Player.email == email)
        ).first()

        if existing_player:
            # Check if already signed up
            existing_signup = PlayerGameSignup.query.filter_by(
                player_id=existing_player.id,
                game_id=current_game.id,
                is_cancelled=False
            ).first()
            
            if existing_signup:
                return jsonify({"error": "Player with this phone or email already signed up!"}), 400

            player = existing_player
            player.name = name  # Update name if changed
            player.signup_status = 'signed up'  # Update status when re-signing up
        else:
            player = Player(name=name, email=email, phone=phone)
            db.session.add(player)

        # Create signup
        signup = PlayerGameSignup(player=player, game=current_game)
        db.session.add(signup)
        
        # Increment player count
        current_game.player_count += 1
        
        db.session.commit()

        # Send notifications in background
        app = current_app._get_current_object()  # Get the actual app object
        threading.Thread(
            target=send_signup_notifications,
            args=(app, player, current_game)
        ).start()

        return jsonify({"message": f"{player.name} has signed up successfully!"}), 201

    except Exception as e:
        current_app.logger.error(f"Error in signup: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

@main.route('/cancel', methods=['POST'])
def cancel():
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"error": "Email is required!"}), 400

        current_game = get_current_game()
        
        # Find the signup
        player = Player.query.filter_by(email=email).first()
        if not player:
            return jsonify({"error": "Player not found!"}), 404

        signup = PlayerGameSignup.query.filter_by(
            player_id=player.id,
            game_id=current_game.id,
            is_cancelled=False
        ).first()

        if not signup:
            return jsonify({"error": "No active signup found!"}), 404

        # Cancel the signup
        signup.is_cancelled = True
        player.signup_status = 'cancelled'
        
        # Increment player count
        current_game.player_count -= 1
        
        db.session.commit()

        # Send notifications in background
        app = current_app._get_current_object()  # Get the actual app object
        threading.Thread(
            target=send_signup_notifications,
            args=(app, player, current_game)
        ).start()

        return jsonify({"message": f"{player.name}'s signup has been canceled!"}), 200

    except Exception as e:
        current_app.logger.error(f"Error in cancel: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

@main.route('/')
def main_page():
    return render_template('main.html')

@main.route('/signup/dashboard')
def signup_dashboard():
    return render_template('signup/dashboard.html')

@main.route('/signup/game/<int:game_id>')
def game_signup(game_id):
    return render_template('signup/game.html')

# @main.route('/test-whatsapp-token')
# def test_whatsapp_token():
#     try:
#         token = current_app.config['WHATSAPP_TOKEN']
#         phone_id = current_app.config['WHATSAPP_PHONE_ID']
        
#         # Basic validation
#         if not token or not phone_id:
#             return jsonify({
#                 "status": "error",
#                 "message": "Missing token or phone ID"
#             }), 400

#         # Log token details (safely)
#         token_info = {
#             "length": len(token),
#             "starts_with": token[:5] if token else None,
#             "contains_whitespace": any(c.isspace() for c in token),
#             "phone_id": phone_id
#         }

#         # Test Graph API directly
#         test_url = "https://graph.facebook.com/v21.0/me"
#         headers = {"Authorization": f"Bearer {token.strip()}"}
        
#         response = requests.get(test_url, headers=headers)
        
#         return jsonify({
#             "status": "info",
#             "token_info": token_info,
#             "test_response": {
#                 "status_code": response.status_code,
#                 "content": response.json() if response.status_code == 200 else response.text
#             }
#         })

#     except Exception as e:
#         current_app.logger.error(f"Token test error: {str(e)}")
#         return jsonify({
#             "status": "error",
#             "message": str(e)
#         }), 500


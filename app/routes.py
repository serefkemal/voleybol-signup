from flask import jsonify, request, render_template, current_app
from app import db
from app.models import Player, WeeklyGame, PlayerGameSignup
from app.utils.validators import validate_email_format, validate_phone_format
from datetime import datetime
import threading

@current_app.route('/')
def signup_form():
    return render_template('signup_form.html')

@current_app.route('/player-count', methods=['GET'])
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

@current_app.route('/signup', methods=['POST'])
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
                return jsonify({"error": "Player already signed up!"}), 400

            player = existing_player
            player.name = name  # Update name if changed
        else:
            player = Player(name=name, email=email, phone=phone)
            db.session.add(player)

        # Create signup
        signup = PlayerGameSignup(player=player, game=current_game)
        db.session.add(signup)
        db.session.commit()

        # Send notifications in background
        threading.Thread(
            target=send_signup_notifications,
            args=(player, current_game)
        ).start()

        return jsonify({"message": f"{player.name} has signed up successfully!"}), 201

    except Exception as e:
        current_app.logger.error(f"Error in signup: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

@current_app.route('/cancel', methods=['POST'])
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
        db.session.commit()

        # Send cancellation notification
        current_app.email_queue.add_to_queue(
            'cancellation_confirmation',
            player.email,
            player_name=player.name,
            game_date=current_game.date.strftime('%A, %B %d, %Y')
        )

        return jsonify({"message": f"{player.name}'s signup has been canceled!"}), 200

    except Exception as e:
        current_app.logger.error(f"Error in cancel: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "An unexpected error occurred"}), 500

def get_current_game():
    current_game = WeeklyGame.query.filter(
        WeeklyGame.date >= datetime.now().date()
    ).first()
    
    if not current_game:
        # Create new game for next Wednesday
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
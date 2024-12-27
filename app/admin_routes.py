from flask import Blueprint, jsonify, request, render_template, session, current_app
from app.extensions import db
from app.models import WeeklyGame, Player, PlayerGameSignup
from functools import wraps
import uuid
from datetime import datetime, timedelta
from flask_login import login_required, current_user


admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/games/<int:game_id>/players')
@login_required
@admin_required
def game_players(game_id):
    signups = PlayerGameSignup.query.filter_by(
        game_id=game_id,
        is_cancelled=False
    ).join(Player).order_by(PlayerGameSignup.signup_time).all()
    
    return jsonify([{
        'id': signup.player.id,
        'name': signup.player.name,
        'email': signup.player.email,
        'phone': signup.player.phone,
        'signup_time': signup.signup_time.isoformat()
    } for signup in signups])

@admin.route('/games/<int:game_id>/details')
@login_required
def game_details(game_id):
    game = WeeklyGame.query.get_or_404(game_id)
    return jsonify(game.to_dict())

@admin.route('/games', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_games():
    if request.method == 'POST':
        current_app.logger.error("games GET/POST:POST")
        data = request.get_json()
        game = WeeklyGame(
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
            location=data['location']
        )
        db.session.add(game)
        db.session.commit()
        return jsonify(game.to_dict())
    
    games = WeeklyGame.query.order_by(WeeklyGame.date).all()
    return jsonify([game.to_dict() for game in games])

@admin.route('/games', methods=['GET'])
@login_required
def get_games():
    current_app.logger.error("games GET:GET")
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        games = WeeklyGame.query.filter(
            WeeklyGame.date >= start,
            WeeklyGame.date <= end
        ).all()

        games_list = []
        for game in games:
            game_dict = game.to_dict()
            # Get active player count
            player_count = PlayerGameSignup.query.filter_by(
                game_id=game.id,
                is_cancelled=False
            ).count()
            game_dict['player_count'] = player_count
            games_list.append(game_dict)
        
        return jsonify(games_list)
        
    except Exception as e:
        current_app.logger.error(f"Error fetching games: {str(e)}")
        return jsonify({"error": "Failed to fetch games"}), 500

@admin.route('/games', methods=['POST'])
@login_required
@admin_required
def create_game():
    try:
        current_app.logger.error("games POST:POST")
        data = request.get_json()
        
        # Parse date and times
        game_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        
        # Check if game already exists on this date
        existing_game = WeeklyGame.query.filter(
            WeeklyGame.date == game_date
        ).first()
        
        if existing_game:
            return jsonify({"error": "A game already exists on this date"}), 400
        
        # Create new game
        game = WeeklyGame(
            date=game_date,
            location=data['location'],
            start_time=start_time,
            end_time=end_time,
            max_players=current_app.config['MAX_PLAYERS']
        )
        
        db.session.add(game)
        db.session.commit()
        
        # Return the created game
        return jsonify(game.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating game: {str(e)}")
        return jsonify({"error": "Failed to create game"}), 500

@admin.route('/games/<int:game_id>', methods=['GET'])
@login_required
@admin_required
def get_game(game_id):
    return render_template('admin/game_dashboard.html')
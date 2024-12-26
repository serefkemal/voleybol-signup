from flask import Blueprint, jsonify, request, render_template, session, current_app
from app import db
from app.models import WeeklyGame, Player, PlayerGameSignup, AdminSession
from functools import wraps
import uuid
from datetime import datetime, timedelta

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = session.get('admin_session_id')
        if not session_id:
            return jsonify({"error": "Not authenticated"}), 401
        
        admin_session = AdminSession.query.filter_by(session_id=session_id).first()
        if not admin_session:
            return jsonify({"error": "Invalid session"}), 401
            
        # Update last activity
        admin_session.last_activity = datetime.utcnow()
        db.session.commit()
        
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
def admin_login():
    return render_template('admin/login.html')

@admin.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    password = data.get('password')
    
    if password == current_app.config['ADMIN_PASSWORD']:
        # Clear old sessions
        AdminSession.clear_old_sessions()
        
        # Create new session
        session_id = str(uuid.uuid4())
        admin_session = AdminSession(session_id=session_id)
        db.session.add(admin_session)
        db.session.commit()
        
        session['admin_session_id'] = session_id
        return jsonify({"success": True})
    
    return jsonify({"error": "Invalid password"}), 401

@admin.route('/dashboard')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/games', methods=['GET', 'POST'])
@admin_required
def manage_games():
    if request.method == 'POST':
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

@admin.route('/games/<int:game_id>/details')
@admin_required
def game_details(game_id):
    game = WeeklyGame.query.get_or_404(game_id)
    return jsonify(game.to_dict())

@admin.route('/games/<int:game_id>/players')
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

@admin.route('/games', methods=['GET'])
@admin_required
def get_games():
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
@admin_required
def create_game():
    try:
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
@admin_required
def get_game(game_id):
    return render_template('admin/game_dashboard.html')
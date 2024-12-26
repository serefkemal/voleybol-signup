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
            name=data['name'],
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

@admin.route('/games/<int:game_id>/players')
@admin_required
def game_players(game_id):
    signups = PlayerGameSignup.query.filter_by(
        game_id=game_id,
        is_cancelled=False
    ).join(Player).all()
    
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
        
        return jsonify([{
            'id': game.id,
            'date': game.date.isoformat(),
            'location': game.location,
            'max_players': game.max_players
        } for game in games])
        
    except Exception as e:
        current_app.logger.error(f"Error fetching games: {str(e)}")
        return jsonify({"error": "Failed to fetch games"}), 500

@admin.route('/games', methods=['POST'])
@admin_required
def create_game():
    data = request.get_json()
    
    try:
        game_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        # Create game with default values
        game = WeeklyGame(
            date=game_date,
            location=current_app.config['DEFAULT_LOCATION'],
            max_players=current_app.config['MAX_PLAYERS'],
            start_time=current_app.config['DEFAULT_GAME_START_TIME'],
            end_time=current_app.config['DEFAULT_GAME_END_TIME']
        )
        
        db.session.add(game)
        db.session.commit()
        
        return jsonify({
            'id': game.id,
            'date': game.date.isoformat(),
            'location': game.location,
            'max_players': game.max_players
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating game: {str(e)}")
        return jsonify({"error": "Failed to create game"}), 500

@admin.route('/games/<int:game_id>', methods=['GET'])
@admin_required
def get_game(game_id):
    return render_template('admin/game_dashboard.html')
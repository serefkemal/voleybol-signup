from flask import Blueprint, jsonify, request, current_app, render_template
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import Player

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/check')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'isAdmin': current_user.is_admin()
        }), 200
    return jsonify({'authenticated': False, 'isAdmin': False}), 401

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    
    data = request.get_json()
    
    if Player.query.filter((Player.phone == data['phone']) | 
                         (Player.email == data['email'])).first():
        return jsonify({"error": "Email or phone already registered"}), 400

    player = Player(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        role='player'
    )
    player.set_password(data['password'])
    
    db.session.add(player)
    db.session.commit()
    
    login_user(player)
    return jsonify({"message": "Signup successful"}), 201

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    data = request.get_json()
    player = Player.query.filter_by(email=data['email']).first()
    
    if player and player.check_password(data['password']):
        login_user(player)
        return jsonify({
            "message": "Login successful",
            "isAdmin": player.is_admin()
        })
    
    return jsonify({"error": "Invalid credentials"}), 401

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})
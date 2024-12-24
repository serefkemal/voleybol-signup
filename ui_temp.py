from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os, threading

# Initialize Flask app and configure
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volleyball.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'voleybol.bilgilendirme@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'mnhw ncxt jgiq gyap'  # Replace with your email password
app.config['MAIL_DEFAULT_SENDER'] = 'voleybol.bilgilendirme@gmail.com'

db = SQLAlchemy(app)
mail = Mail(app)

# Database model
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(10), default='signed up')

# Initialize database
with app.app_context():
    db.create_all()

# Utility function to send email
def send_email(subject, recipient, body):
    try:
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Signup form route
@app.route('/')
def signup_form():
    return render_template('signup_form.html')

# Handle form submission
@app.route('/signup_form', methods=['POST'])
def signup():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # Basic validation
    if not name or not email or not phone:
        return render_template('signup_form.html', message="All fields are required!")

    # Check if player already exists
    existing_player = Player.query.filter((Player.phone == phone) | (Player.email == email)).first()
    if existing_player:
        return render_template('signup_form.html', message="Player with this phone or email already signed up!")

    # Add new player to the database
    player = Player(name=name, phone=phone, email=email)
    db.session.add(player)
    db.session.commit()

    # Send a confirmation email to the user (using background thread)
    threading.Thread(target=send_email, args=("Volleyball Sign-Up Confirmation", email, f"Hi {name},\n\nThank you for signing up!")).start()

    return render_template('signup_form.html', message=f"{name}, you have successfully signed up!")

if __name__ == '__main__':
    app.run(debug=True)

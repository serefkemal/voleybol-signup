from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os, threading

organizers = ['serefkemal@gmail.com']

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///volleyball.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

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

# Utility function to send emails
def send_email(subject, recipient, body):
    try:
        msg = Message(subject, recipients=[recipient])
        msg.body = body
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# Utility function to send sign-up notifications
def send_signup_notifications(player):
    # Use the app context for background threads
    with app.app_context():
        # Send email notification to the player
        if player.status == 'signed up':
            email_subject = "Volleyball Sign-Up Confirmation"
            email_body = f"Hi {player.name},\n\nThank you for signing up for the weekly volleyball game!"
        elif player.status == 'canceled':
            email_subject = "Volleyball Cancelation Confirmation"
            email_body = f"Hi {player.name},\n\nThank you for canceling for the weekly volleyball game."
        
        send_email(email_subject, player.email, email_body)

        # Send notification to organizers
        send_organizer_notification()

# Signup form route
@app.route('/')
def signup_form():
    return render_template('signup_form.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.json.get('name')
    email = request.json.get('email')
    phone = request.json.get('phone')

    print(f"Received data - Name: {name}, Email: {email}, Phone: {phone}")
    
    # Basic validation
    if not name or not email or not phone:
        return jsonify({"error": "All fields are required!"}), 400

    # Check if the player already exists
    existing_player = Player.query.filter((Player.phone == phone) | (Player.email == email)).first()
    if existing_player:
        if existing_player.status == 'canceled':
            # Update existing player to re-sign up
            existing_player.name = name
            existing_player.email = email
            existing_player.status = 'signed up'
            db.session.commit()

            threading.Thread(target=send_signup_notifications, args=(existing_player,)).start()
            return jsonify({"message": f"{existing_player.name} has re-signed up successfully!"}), 200

        # Already signed up case
        return jsonify({"error": "Player with this phone or email already signed up!"}), 400

    # Add the new player
    player = Player(name=name, phone=phone, email=email)
    db.session.add(player)
    db.session.commit()

    threading.Thread(target=send_signup_notifications, args=(player,)).start()
    return jsonify({"message": f"{player.name} has signed up successfully!"}), 201


# Endpoint to cancel sign-up
@app.route('/cancel', methods=['POST'])
def cancel():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    
    print(f"Received data - Name: {name}, Email: {email}, Phone: {phone}")
    
    if not email:
        return render_template('signup_form.html',message="Phone number is required!"),400

    # Find and update the player's status
    player = Player.query.filter_by(email=email).first()
    if player:
        player.status = 'canceled'
        db.session.commit()

        # Respond immediately to the user
        response_message = {"message": f"{player.name}'s sign-up has been canceled!"}
        threading.Thread(target=send_signup_notifications, args=(player,)).start()
        return render_template('signup_form.html',message=response_message), 201

    return render_template('signup_form.html',message="Player not found!"),404

# Utility function to send organizer notification
def send_organizer_notification():
    players = Player.query.filter_by(status='signed up').all()
    signed_players = [player.name for player in players]

    email_subject = "Weekly Volleyball Organizer: Roster Update"
    email_body = f"Here is the list of currently signed-up players:\n\n" + "\n".join(signed_players)

    for organizer in organizers:
        send_email(email_subject, organizer, email_body)  # Replace with organizer's email


if __name__ == "__main__":
    app.run(debug=True)

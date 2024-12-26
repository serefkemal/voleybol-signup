from datetime import datetime, timedelta
from app import db  # Update this line

class WeeklyGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    player_count = db.Column(db.Integer, default=0)
    max_players = db.Column(db.Integer, default=12)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.date().isoformat(),
            'location': self.location,
            'player_count': self.player_count,
            'max_players': self.max_players,
            'start_time': self.start_time.strftime('%H:%M') if self.start_time else None,
            'end_time': self.end_time.strftime('%H:%M') if self.end_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    signup_status = db.Column(db.String(20), default='signed up')  # 'signed up' or 'cancelled'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PlayerGameSignup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('weekly_game.id'), nullable=False)
    signup_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_cancelled = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    player = db.relationship('Player', backref=db.backref('signups', lazy=True))
    game = db.relationship('WeeklyGame', backref=db.backref('signups', lazy=True))

class AdminSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def clear_old_sessions():
        # Clear sessions older than 24 hours
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        AdminSession.query.filter(AdminSession.last_activity < one_day_ago).delete()
        db.session.commit()
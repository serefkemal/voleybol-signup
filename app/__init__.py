from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from app.config import Config
from app.utils.logging_config import setup_logging
from app.models import Player
import os
from app.extensions import db, mail, login_manager
from datetime import timedelta

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    # Initialize Flask extensions
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return Player.query.get(int(id))
    # Setup logging
    setup_logging(app)

    from app.routes import main
    from app.admin_routes import admin
    from app.auth_routes import auth
    
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(auth)

    with app.app_context():
        # Create database tables
        db.create_all()
        # Initialize database
        from app.database_init import init_db
        init_db()
        
        # Initialize email queue
        from app.utils.email_queue import EmailQueue
        app.email_queue = EmailQueue(app, mail)

    return app
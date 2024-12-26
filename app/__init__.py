from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from app.config import Config
from app.utils.logging_config import setup_logging
import os

# Initialize extensions
db = SQLAlchemy()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    mail.init_app(app)

    # Setup logging
    setup_logging(app)

    from app.routes import main
    from app.admin_routes import admin
    
    app.register_blueprint(main)
    app.register_blueprint(admin)

    with app.app_context():
        # Create database tables
        db.create_all()

        # Initialize email queue
        from app.utils.email_queue import EmailQueue
        app.email_queue = EmailQueue(app, mail)

    return app
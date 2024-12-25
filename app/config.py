# config.py
import os
from datetime import time

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///volleyball.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    
    # Game Settings
    DEFAULT_GAME_START_TIME = time(19, 0)  # 7:00 PM
    DEFAULT_GAME_END_TIME = time(21, 0)    # 9:00 PM
    DEFAULT_LOCATION = "Main Volleyball Court"
    MAX_PLAYERS = 14
    
    # Logging
    LOG_FILE = 'volleyball.log'

    # Organizers
    ORGANIZERS = ['serefkemal@gmail.com']
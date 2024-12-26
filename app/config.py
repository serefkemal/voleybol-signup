# config.py
import os
from datetime import time

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    
    # Game Settings
    DEFAULT_GAME_START_TIME = time(21, 0)  # 9:00 PM
    DEFAULT_GAME_END_TIME = time(23, 0)    # 11:00 PM
    DEFAULT_LOCATION = "Hüseyin Avni Sözen Anadolu Lisesi"
    MAX_PLAYERS = 12
    
    # Logging
    LOG_FILE = 'volleyball.log'

    # Organizers
    ORGANIZERS = ['serefkemal@gmail.com']
    
    # WhatsApp Configuration
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    WHATSAPP_ENABLED = os.getenv('WHATSAPP_ENABLED', 'False').lower() == 'true'
    WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')
    
    # Admin
    ADMIN_PASSWORD=os.getenv('ADMIN_PASSWORD')
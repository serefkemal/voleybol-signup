import os
from datetime import time, timedelta

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
    
    # Auth
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_REFRESH_EACH_REQUEST = True
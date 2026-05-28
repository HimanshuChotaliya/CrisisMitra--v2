import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'HIMANSHU')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///crisismitra.db')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'HIMANSHU')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    
    # Admin Credentials loaded from environment
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@gmail.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '@dmin')
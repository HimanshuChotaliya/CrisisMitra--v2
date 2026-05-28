import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

database_url = os.environ.get('DATABASE_URL', 'sqlite:///crisismitra.db')

# Railway/Render gives postgres://, but SQLAlchemy 1.4+ requires postgresql://
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'HIMANSHU')
    SQLALCHEMY_DATABASE_URI = database_url
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'HIMANSHU')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    
    # Admin Credentials loaded from environment
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@gmail.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '@dmin')

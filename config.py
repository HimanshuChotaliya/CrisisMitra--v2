import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'HIMANSHU')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'HIMANSHU')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False
from flask import Flask
from app.extensions import db, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.models import User, Sos, Volunteer, Skill
        db.create_all()



    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    from app.blueprints.volunteer import volunteer_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(volunteer_bp)

    return app

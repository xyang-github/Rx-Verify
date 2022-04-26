from flask import Flask
from flask_bootstrap import Bootstrap
from config import *
from flask_mail import Mail
from flask_login import LoginManager


# Start initializing extensions here
bootstrap = Bootstrap()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """Factory function for application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Finish initializing extensions here
    bootstrap.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register blueprints to app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    from .db import db as db_blueprint
    app.register_blueprint(db_blueprint)

    from .interaction import interaction as interaction_blueprint
    app.register_blueprint(interaction_blueprint)

    return app

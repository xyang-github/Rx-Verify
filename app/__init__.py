from flask import Flask
from flask_bootstrap import Bootstrap
from config import *


# Start initializing extensions here
bootstrap = Bootstrap()


def create_app(config_name):
    """Factory function for application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Finish initializing extensions here
    bootstrap.init_app(app)

    # Register blueprints to app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint)

    return app

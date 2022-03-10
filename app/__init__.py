from flask import Flask
from config import config

# Start initializing extensions here

def create_app(config_name):
    """Factory function for application"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # Apply configuration file here

    # Finish initializing extensions here
    config[config_name].init_app(app)

    # Register blueprints to app

    return app

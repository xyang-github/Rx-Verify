import os

class Config:
    """Default configuration settings"""
    SECRET_KEY = "e5b4dea1e8e4f81c044dc2c5a36ce9608de780409d6bf8847bd1fe2ced4edc3f"


class DevelopmentConfig(Config):
    """Additional configuration setting for app development"""
    DEBUG = True


class TestingConfig(Config):
    """Additional configuration setting for app testing"""
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
import os


class Config:
    """Default configuration settings"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e5b4dea1e8e4f81c044dc2c5a36ce9608de780409d6bf8847bd1fe2ced4edc3f'
    LOGIN_MAIL_SUBJECT_PREFIX = '[Company]'
    LOGIN_ADMIN = os.environ.get('LOGIN_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Additional configuration setting for app development"""
    DEBUG = True

    # Mail config
    LOGIN_MAIL_SENDER = 'LOGIN ADMIN <0c6e22c1b5-f075dd@inbox.mailtrap.io>'
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'b4cdd9e31c1cfc'
    MAIL_PASSWORD = '1b16b9aeffcc0e'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


class TestingConfig(Config):
    """Additional configuration setting for app testing"""
    TESTING = True
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

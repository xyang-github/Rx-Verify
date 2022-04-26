import os


class Config:
    """Default configuration settings"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e5b4dea1e8e4f81c044dc2c5a36ce9608de780409d6bf8847bd1fe2ced4edc3f'
    WTF_CSRF_ENABLED = True

    # Mail config
    LOGIN_MAIL_SENDER = 'LOGIN ADMIN <rxverify.cs195@gmail.com>'
    LOGIN_MAIL_SUBJECT_PREFIX = '[Rx Verify]'
    LOGIN_ADMIN = os.environ.get('LOGIN_ADMIN')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'rxverify.cs195@gmail.com'
    MAIL_PASSWORD = 'nfhkrljawqbswlvi'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """Additional configuration setting for app development"""
    DEBUG = True


class TestingConfig(Config):
    """Additional configuration setting for app testing"""
    TESTING = True
    WTF_CSRF_ENABLED = False
    LOGIN_DISABLED = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

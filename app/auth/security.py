from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email, password_hash, confirmed):
        self.id = id
        self.email = email
        self.password_hash = password_hash


class Security:
    def generate_password_hash(self, password):
        """Create a hash for the password"""
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def verify_password(self, hash_password, password):
        """Verify that password matches the hash"""
        return check_password_hash(hash_password, password)

    def generate_configuration_token(self, id, expiration=600):
        """Create a token to confirm registration"""
        serializer = Serializer(current_app.config['SECRET_KEY'], expiration)
        return serializer.dumps({'confirm': id}).decode('utf-8')

    def confirm(self, id, token):
        """If confirmation token is valid, will change 'confirmed' value to True"""
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != id:
            return False
        else:
            return True


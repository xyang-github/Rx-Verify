from werkzeug.security import check_password_hash, generate_password_hash

from app.auth.security import Security


def test_token_generation():
    """Test to make sure a token is generated with a given string"""
    password_hash = generate_password_hash("StarFish123!")
    assert len(password_hash) > 0


def test_verify_password():
    """Test to make sure verify password feature works"""
    password_hash = generate_password_hash("StarFish123!")
    assert check_password_hash(password_hash, "StarFish123!") == True
    assert check_password_hash(password_hash, "Starfish") == False


def test_configuration_token():
    """Test that a configuration token is generated"""
    token = Security().generate_configuration_token(1)
    assert len(token) > 0


def test_confirm_configuration_token():
    """Test that confirming the configuration token works"""
    token = Security().generate_configuration_token(1)
    confirmed = Security().confirm(1, token)
    assert confirmed == True




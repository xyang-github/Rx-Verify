import sqlite3
from werkzeug.security import generate_password_hash

# path_dev = 'app/db/db.db'
from app.db.database_queries import query_change


def add_user():
    """Will add a new user and patient to the test database"""

    password = "Catfish000!"
    password_hash = generate_password_hash(password)
    email = "123@hotmail.com"

    # Add new user
    query_change(
        query="INSERT INTO user (email, password, confirmed) VALUES (?, ?, ?)",
        key=[email, password_hash, 1]
    )

    # Add new patient
    query_change(
        query="INSERT INTO patient (patient_id, user_id, fname, lname, dob) VALUES (?, ?, ?, ?, ?)",
        key=[1, 1, "John", "Doe", "01-01-2022"]
    )


def test_login_route(test_client):
    """Test login page loads"""
    response = test_client.post("/login")
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_feature(test_client):
    """Test that login feature works and redirects accordingly"""

    add_user()

    data = {
        "email": "123@hotmail.com",
        "password": "Catfish000!"
    }

    response = test_client.post("/login", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Profile' in response.data
    assert len(response.history) == 1


def test_wrong_password(test_client):
    """Test that validation works for incorrect password"""

    add_user()

    data = {
        "email": "123@hotmail.com",
        "password": "wrong password"
    }

    response = test_client.post("/login", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid password' in response.data
    assert len(response.history) == 0


def test_wrong_email(test_client):
    """Test that validation works for incorrect email"""

    add_user()

    data = {
        "email": "wrong@hotmail.com",
        "password": "Catfish000!"
    }

    response = test_client.post("/login", data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid email' in response.data
    assert len(response.history) == 0
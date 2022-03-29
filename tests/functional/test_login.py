import sqlite3
from flask import session

from app.auth.security import Security
from rx_verify import app

path_dev = 'app/db/db.db'


def test_login_route(test_client):
    """
    GIVEN a flask application
    WHEN the '/login' page is posted
    THEN check that response is valid
    """
    response = test_client.post("/login")
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_feature(test_client):
    """
    GIVEN a flask application
    WHEN trying to login with correct credentials
    THEN check that response is valid
    """

    password_hash = Security().generate_password_hash("Catfish110!")
    con = sqlite3.connect(path_dev)
    cur = con.cursor()
    cur.execute("INSERT INTO user (email, password) VALUES (?, ?)", ["123@hotmail.com", password_hash])
    con.commit()
    con.close()

    data = {
        "email": "123@hotmail.com",
        "password": "Catfish110!"
    }
    response = test_client.post("/login", data=data)

    print(response.data)
    assert response.status_code == 200
    assert b'Profile' in response.data


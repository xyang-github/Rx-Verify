import sqlite3
from werkzeug.security import generate_password_hash

path_dev = 'app/db/db.db'


def test_login_route(test_client):
    """Test login page loads"""
    response = test_client.post("/login")
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login_feature(test_client):
    """Test that login feature works"""
    password = "Catfish110"
    password_hash = generate_password_hash(password)
    email = "123@hotmail.com"

    con = sqlite3.connect(path_dev)
    cur = con.cursor()
    cur.execute("INSERT INTO user (email, password) VALUES (?, ?)", [email, password_hash])
    con.commit()
    con.close()

    data = {
        "email": email,
        "password": password
    }
    response = test_client.post("/login", data=data)

    assert response.status_code == 302


def test_login_validation(test_client):
    """Test that validation for incorrect email and password works"""
    password = "Catfish110"
    password_hash = generate_password_hash(password)
    email = "123@hotmail.com"

    con = sqlite3.connect(path_dev)
    cur = con.cursor()
    cur.execute("INSERT INTO user (email, password) VALUES (?, ?)", [email, password_hash])
    con.commit()
    con.close()

    data = {
        "email": "1234@hotmail.com",
        "password": password
    }
    response = test_client.post("/login", data=data)
    html = response.get_data(as_text=True)

    assert 'Invalid email' in html

    data = {
        "email": email,
        "password": "wrong password"
    }

    response = test_client.post("/login", data=data)
    html = response.get_data(as_text=True)
    print(html)

    assert 'Invalid password' in html


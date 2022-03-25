from flask import session

from rx_verify import app


def test_register_page_load(test_client):
    """
    GIVEN a flask application
    WHEN the '/register' page is posted
    THEN check that response is valid
    """

    response = test_client.post("/register")
    assert response.status_code == 200
    assert b'Register' in response.data


def test_duplicate_email_registration(test_client):
    """
    GIVEN a user registration
    WHEN trying to register with an already existing email in the database
    THEN check that no new entry is added
    """

    data = {
        "email": "123@hotmail.com",
        "fname": "John",
        "lname": "Doe",
        "minitial": "",
        "dob": "02-28-1989",
        "weight": "117",
        "allergies": "",
        "password": "Starfish110!",
        "password2": "Starfish110!"
    }

    response = test_client.post('/register', data=data, follow_redirects=True)
    print(session['email'])
    # assert b'Email already registered' in response.data
    assert response.status_code == 200
    assert b'Email already registered' in response.data
    assert session['email'] == "123@hotmail.com"





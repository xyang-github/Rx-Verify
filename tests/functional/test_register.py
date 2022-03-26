import sqlite3
from flask import session
from rx_verify import app

path_dev = 'app/db/db.db'
path_test = 'app/db/test.db'

def test_register_page_load(test_client):
    """
    GIVEN a flask application
    WHEN the '/register' page is posted
    THEN check that response is valid
    """

    response = test_client.post("/register")
    assert response.status_code == 200
    assert b'Register' in response.data


def test_password_field(test_client):
    """
    GIVEN a user registration
    WHEN trying to register with non-matching passwords, or passwords not meeting requirements
    THEN check that an error message is displayed
    """

    data = {"password": "Starfish110!", "password2": "Star!"}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'Passwords must match.' in response.data

    data = {"password": "cat", "password2": "cat"}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'Password must have at least 8 characters and include: 1 uppercase letter,' in response.data


def test_blank_email_field(test_client):
    """
    GIVEN a user registration
    WHEN trying to register with blank email field
    THEN check that an error message is displayed
    """
    data = {"email": ""}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'Email cannot be blank' in response.data


def test_allergy_field(test_client):
    """
    GIVEN a user registration
    WHEN trying to register with allergies not meeting regex requirements
    THEN check that an error message is displayed
    """
    data = {"allergies": "penicillin, lisinopril, atorvastatin"}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'Allergies can only contain letters and spaces' in response.data


def test_allergy_table():
    """
    GIVEN a list of duplicate values
    WHEN writing the list of duplicate values to the database with a unique constraint
    THEN check that the only one instance of the value is written
    """
    con = sqlite3.connect(path_test)
    cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO patient_allergy (patient_id, allergy) VALUES (1, 'cat')")
    con.commit()
    cur.execute("INSERT OR IGNORE INTO patient_allergy (patient_id, allergy) VALUES (1, 'cat')")
    con.commit()
    cur.execute("SELECT allergy FROM patient_allergy WHERE patient_id = 1")
    result = cur.fetchall()
    con.close()

    assert len(result) == 1


def test_name_fields(test_client):
    """
    GIVEN a user registration
    WHEN trying to register with blank first and last name fields
    THEN check that an error message is displayed
    """

    data = {"fname": "", "lname": ""}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'First name cannot be blank' in response.data
    assert b'Last name cannot be blank' in response.data

    data = {"fname": "John", "lname": ""}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'Last name cannot be blank' in response.data

    data = {"fname": "", "lname": "Doe"}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'First name cannot be blank' in response.data


def test_duplicate_email(test_client):
    """
    GIVEN a user registration
    WHEN trying to register with a duplicate email
    THEN check that an error message is displayed
    """

    con = sqlite3.connect(path_dev)
    cur = con.cursor()
    cur.execute("INSERT INTO user (email, password) VALUES ('123@yahoo.com', 'cat')")
    con.commit()
    con.close()

    data = {"email": "123@yahoo.com",
            "fname": "John",
            "lname": "Doe",
            "dob": "1989-02-28",
            "password": "Starfish110!",
            "password2": "Starfish110!"}

    response1 = test_client.post('/register', data=data, follow_redirects=True)
    html = response1.get_data(as_text=True)

    con = sqlite3.connect(path_dev)
    cur = con.cursor()
    cur.execute("DELETE FROM user WHERE email = '123@yahoo.com'")
    con.commit()
    con.close()

    assert 'Email already registered' in html


# def test_correct_registration(test_client):
#
#     data = {"email": "123@yahoo.com",
#             "fname": "John",
#             "lname": "Doe",
#             "dob": "1989-02-28",
#             "password": "Starfish110!",
#             "password2": "Starfish110!",
#             "allergies": "penicillin"}
#
#     response = test_client.post('/register', data=data, follow_redirects=True)
#     html = response.get_data(as_text=True)
#
#     con = sqlite3.connect(path_dev)
#     cur = con.cursor()
#     cur.execute("DELETE FROM user WHERE email = '1234@yahoo.com'")
#     con.commit()
#     con.close()
#
#     assert response.status_code == 200
#     assert 'A confirmation email has been sent' in html
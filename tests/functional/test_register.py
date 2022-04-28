import sqlite3
path_dev = 'app/db/db.db'
path_test = 'app/db/test.db'


def test_register_page_load(test_client):
    """Test that the registration page is loaded"""
    response = test_client.post("/register")
    assert response.status_code == 200
    assert b'Register' in response.data


def test_password_field(test_client):
    """Test that validation for the password form field is working"""
    data = {"password": "Starfish110!", "password2": "Star!"}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'Passwords must match.' in response.data

    data = {"password": "cat", "password2": "cat"}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'Password must have at least 8 characters and include: 1 uppercase letter,' in response.data


def test_blank_email_field(test_client):
    """Test that validation for the email form field is working"""
    data = {"email": ""}
    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'Email cannot be blank' in response.data


def test_allergy_field(test_client):
    """Test that validation for the allergy form field is working"""
    data = {"email": "123@yahoo.com",
            "fname": "John",
            "lname": "Doe",
            "dob": "1989-02-28",
            "password": "Starfish110!",
            "password2": "Starfish110!",
            "allergies": "penicillin, lisinopril, atorvastatin, 1234"}

    response = test_client.post('/register', data=data, follow_redirects=True)
    assert b'Allergies can only contain letters, commas, and spaces' in response.data


def test_allergy_table():
    """Test that the database is only writing unique allergies when the form field contains duplicate entries"""
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


def test_blank_name_fields(test_client):
    """Test that first and last name form fields cannot be blank"""
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
    """Test that a warning is raised when trying to register with an email that is already in the database"""

    con = sqlite3.connect(path_test)
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

    response = test_client.post('/register', data=data, follow_redirects=True)

    assert b'Email already registered' in response.data
    assert response.status_code == 200
    assert len(response.history) == 1


def test_correct_registration(test_client):
    """Test that a confirmation email is sent when registering"""

    data = {"email": "12345@yahoo.com",
            "fname": "John",
            "lname": "Doe",
            "minitial": "",
            "dob": "1989-02-28",
            "weight": "",
            "allergies": "",
            "password": "AbcdeFG111!",
            "password2": "AbcdeFG111!"}

    response = test_client.post('/register', data=data, follow_redirects=True)

    assert response.status_code == 200
    assert b'A confirmation email has been sent' in response.data
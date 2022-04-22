from app.db.database_queries import query_change, query_select


def test_profile_main(test_client):
    """Test that main profile page loads"""
    query_change(
        query="INSERT INTO patient (patient_id, user_id, fname, lname, dob) VALUES (?, ?, ?, ?, ?)",
        key=[1, 1, "John", "Doe", "02-28-1989"]
    )

    # Source: https://stackoverflow.com/questions/43104688/accessing-session-object-during-unit-test-of-flask-application
    with test_client.session_transaction() as session:
        session['patient_id'] = 1

    response = test_client.get("/profile", follow_redirects=True)
    assert response.status_code == 200
    assert b'Profile' in response.data
    assert b'John' in response.data


def test_edit_profile(test_client):
    """Test that edit profile page loads"""

    query_change(
        query="INSERT INTO patient (patient_id, user_id, fname, lname, dob) VALUES (?, ?, ?, ?, ?)",
        key=[1, 1, "John", "Doe", "02-28-1989"]
    )

    with test_client.session_transaction() as session:
        session['patient_id'] = 1

    response = test_client.get("/edit")

    assert response.status_code == 200
    assert b'Update Profile' in response.data
    assert b'John' in response.data


def test_edit_information(test_client):
    """Test that submitting an updated profile will redirect correctly"""

    query_change(
        query="INSERT INTO patient (patient_id, user_id, fname, lname, dob) VALUES (?, ?, ?, ?, ?)",
        key=[1, 1, "John", "Doe", "02-28-1989"]
    )

    with test_client.session_transaction() as session:
        session['patient_id'] = 1

    data = {
        "fname": "Jane",
        "lname": "Doe",
        "minitial": "",
        "dob": "1989-02-28",
        "weight": "",
        "allergies": ""
    }

    response = test_client.post('/edit', data=data, follow_redirects=True)
    print(response.data)

    assert response.status_code == 200
    assert b'Profile has been updated' in response.data



# Test cancel button works

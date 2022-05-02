from app.db.database_queries import query_change


def add_patient(test_client):
    """Add a patient to the patient table and set the patient_id value for the session"""
    query_change(
        query="INSERT INTO patient (patient_id, user_id, fname, lname, dob) VALUES (?, ?, ?, ?, ?)",
        key=[1, 1, "John", "Doe", "02-28-1989"]
    )

    # Source:
    # https://stackoverflow.com/questions/43104688/accessing-session-object-during-unit-test-of-flask-application
    with test_client.session_transaction() as session:
        session['patient_id'] = 1


def add_medication():
    """Add a medication into the active medication table"""
    query_change(
        query="INSERT INTO active_med (patient_id, med_name, med_dose, med_directions, rxcui) VALUES (?, ?, ?, ?, ?)",
        key=[1, 'Lisinopril (Oral Pill)', '30 mg Tab', '1 tab daily', '205326']
    )


def test_medication_page_load(test_client):
    """Test that medication page loads"""
    add_patient(test_client)

    response = test_client.get("/medmain", follow_redirects=True)
    assert response.status_code == 200
    assert b'Medication' in response.data
    assert b'No Active Medications On File' in response.data
    assert b'No Historical Medications On File' in response.data


def test_add_med_load(test_client):
    """Test that the add new medication page loads"""
    add_patient(test_client)

    response = test_client.get("/med_add", follow_redirects=True)
    assert response.status_code == 200
    assert b'Add New Medication' in response.data


def test_add_med_cancel_btn(test_client):
    """Test that the cancel button redirects to the main page"""
    add_patient(test_client)

    data = {
        "cancel_btn": True
    }

    response = test_client.post('/med_add', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Medication' in response.data
    assert b'No Active Medications On File' in response.data


def test_add_med_add_btn(test_client):
    """Test that the add button works"""
    add_patient(test_client)

    data = {
        "rxterms": "Lisinopril (Oral Pill)",
        "drug_strengths": "10 mg Tab",
        "med_directions": "take 1 tab by mouth daily",
        "add_btn": True,
    }

    response = test_client.post('/med_add', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Medication' in response.data
    assert b'Lisinopril (Oral Pill)' in response.data


def test_edit_med_load(test_client):
    """Test that the edit medication page loads"""
    add_patient(test_client)
    add_medication()

    response = test_client.get('/med_edit/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Lisinopril (Oral Pill)' in response.data


def test_edit_med_update(test_client):
    """Test that the edit medication's update button works"""
    add_patient(test_client)
    add_medication()

    data = {
        "rxterms": "Lisinopril (Oral Pill)",
        "drug_strengths": "10 mg Tab",
        "med_directions": "1 tab daily",
        "start_date": "",
        "comment": "",
        "update_btn": True
    }

    response = test_client.post('/med_edit/1', data=data, follow_redirects=True)
    assert b'10 mg Tab' in response.data


def test_edit_med_toggle(test_client):
    """Test that toggling of active medication to historical medication works"""
    add_patient(test_client)
    add_medication()

    data = {
        "toggle_btn": True
    }

    response = test_client.post('/med_edit/1', data=data, follow_redirects=True)
    assert b'Active medication has been moved historical medications' in response.data





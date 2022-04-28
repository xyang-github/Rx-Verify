def test_page_loads(test_client):
    """Test that the drug interaction page is loaded"""
    response = test_client.post("/interaction")
    assert response.status_code == 200
    assert b'Drug Interaction' in response.data


def test_no_med_entered(test_client):
    """Test that a message is shown if the submit button is clicked with less than two medications listed"""
    data = {
        'btn_submit': True
    }

    response = test_client.post("/interaction", data=data, follow_redirects=True)
    assert b'Must enter at least two medications to run an interaction' in response.data


def test_no_med_added(test_client):
    """Test that a message is shown if the add button is clicked when the input is blank"""

    data = {
        'rxterms': "",
        'btn_add': True
    }

    response = test_client.post("/interaction", data=data, follow_redirects=True)
    assert b'Medication name cannot be blank' in response.data


def test_add_med(test_client):
    """Test that adding a medication will make it appear in the select input"""

    data = {
        'rxterms': 'Aspirin (Oral Pill)',
        'btn_add': True,
    }

    response = test_client.post("/interaction", data=data)
    assert b'Aspirin (Oral Pill)' in response.data


def test_failed_drug_interaction(test_client):
    """Test clicking the submit button when there is less than two medications"""

    data = {
        'rxterms': 'Aspirin (Oral Pill)',
        'btn_add': True,
    }

    response = test_client.post("/interaction", data=data, follow_redirects=True)

    data2 = {
        'btn_submit': True
    }

    response2 = test_client.post("/interaction", data=data2, follow_redirects=True)
    assert b'Must enter at least two medications to run an interaction' in response2.data


def test_no_drug_interaction(test_client):
    """Test a submission that has no drug interaction"""
    data = {
        'rxterms': 'Simethicone (Chewable)',
        'btn_add': True
    }

    response = test_client.post("/interaction", data=data, follow_redirects=True)

    data2 = {
        'rxterms': 'Aspirin (Oral Pill)',
        'btn_add': True,
        'btn_submit': True
    }

    response2 = test_client.post("/interaction", data=data2, follow_redirects=True)
    assert b'There is no reported drug interaction' in response2.data


def test_one_drug_interaction(test_client):
    """Test a submission that has one drug interaction"""
    data = {
        'rxterms': 'Lisinopril (Oral Pill)',
        'btn_add': True
    }

    response = test_client.post("/interaction", data=data, follow_redirects=True)

    data2 = {
        'rxterms': 'Lithium carbonate XR (Oral Pill)',
        'btn_add': True,
        'btn_submit': True
    }

    response2 = test_client.post("/interaction", data=data2, follow_redirects=True)
    assert b'The serum concentration of Lithium carbonate can be increased when it is combined with Lisinopril.' \
           in response2.data


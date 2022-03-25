def test_edit_button(test_client):
    """
    GIVEN a flask application
    WHEN the '/edit' page is posted
    THEN check that response is valid
    """

    response = test_client.post("/edit")
    assert response.status_code == 200
    assert b'Update Profile' in response.data


def test_edit_profile(test_client):  # not working yet
    """
    GIVEN a flask application
    WHEN the '/edit' page is posted with forms filled
    THEN check that response is valid
    """

    response = test_client.post("/edit", data={
        "fname": "Xing",
        "lname": "Yang",
        "minitial": "",
        "dob": "02-28-1989",
        "weight": "abc"
    })
    assert response.status_code == 200
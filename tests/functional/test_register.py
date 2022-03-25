def test_register_page_load(test_client):
    """
    GIVEN a flask application
    WHEN the '/register' page is posted
    THEN check that response is valid
    """

    response = test_client.post("/register")
    assert response.status_code == 200
    assert b'Register' in response.data
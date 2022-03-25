def test_main_page(test_client):
    """
    GIVEN a flask application
    WHEN the '/' page is posted
    THEN check that response is valid
    """
    response = test_client.post("/")
    assert response.status_code == 200
    assert b'Rx Verify' in response.data

from app.db.database_queries import query_change


def test_forgot_password_page(test_client):
    """Test that the forgot password page loads"""
    response = test_client.post("/forgot_password")
    assert response.status_code == 200
    assert b'Find Your Account' in response.data


def test_retrieve_email(test_client):
    """Test that submitting a valid email works"""
    email = "123@hotmail.com"
    query_change(
        query="INSERT INTO user (email, password, confirmed) VALUES (?, ?, ?)",
        key=[email, "password", 1]
    )

    response = test_client.post("/forgot_password", data={"email": email})
    assert response.status_code == 302
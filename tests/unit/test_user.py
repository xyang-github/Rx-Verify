from app.auth.views import load_user
from app.db.database_queries import query_change, query_select


def test_load_user():
    """test that the load_user function works"""
    email = "123@hotmail.com"
    query_change(
        query="INSERT INTO user (email, password, confirmed) VALUES (?, ?, ?)",
        key=[email, "password", 1]
    )

    result = query_select(
        query="SELECT user_id FROM user WHERE email = (?)",
        key=email
    )

    user = load_user(result[0][0])
    assert user.id == result[0][0]

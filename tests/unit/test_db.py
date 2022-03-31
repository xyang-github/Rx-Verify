from app.db.database_queries import query_select, query_change


def test_change():
    """Test that writing to the database using a custom function works"""
    try:
        query_change(
            query="INSERT INTO user (email, password) VALUES (?, ?)",
            key=["123@hotmail.com", "password"]
        )
    except:
        assert False


def test_select():
    """Test that selecting from the database using a custom function works"""
    query_change(
        query="INSERT INTO user (email, password) VALUES (?, ?)",
        key=["123@hotmail.com", "password"]
    )

    result = query_select(
        query="SELECT * FROM user WHERE email = (?)",
        key="123@hotmail.com"
    )

    assert result[0][1] == "123@hotmail.com"
    assert result[0][2] == "password"

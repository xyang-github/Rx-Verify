import pytest as pytest
import sqlite3
from app import create_app

@pytest.fixture(scope="module")
def test_client():
    app = create_app("testing")

    # Execute sql file
    # Source: https://stackoverflow.com/questions/54289555/how-do-i-execute-an-sqlite-script-from-within-python

    with app.test_client() as test_client:
        ctx = app.app_context()
        ctx.push()

        yield test_client

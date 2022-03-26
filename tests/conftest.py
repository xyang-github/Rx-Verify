import pytest as pytest
import sqlite3
from app import create_app

@pytest.fixture(scope="function")
def test_client():
    app = create_app("testing")

    # Execute sql file
    # Source: https://stackoverflow.com/questions/54289555/how-do-i-execute-an-sqlite-script-from-within-python

    with app.test_client() as test_client:
        ctx = app.app_context()
        ctx.push()

        with app.open_resource('db/schema.sql', mode='r') as f:
            con = sqlite3.connect('app/db/test.db')
            cur = con.cursor()
            cur.executescript(f.read())
            con.commit()
            con.close()

        yield test_client

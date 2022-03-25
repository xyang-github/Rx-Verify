import pytest as pytest
import sqlite3
from app import create_app

@pytest.fixture(scope="module")
def test_client():
    app = create_app("testing")

    # Execute sql file
    # Source: https://stackoverflow.com/questions/54289555/how-do-i-execute-an-sqlite-script-from-within-python
    with open('app/db/schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    db = sqlite3.connect('app/db/test.db')
    cursor = db.cursor()
    cursor.executescript(sql_script)
    db.commit()
    db.close()

    with app.test_client() as test_client:

        yield test_client

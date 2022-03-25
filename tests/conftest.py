import pytest as pytest
import sqlite3
from app import create_app
path = 'app/db/test.db'

@pytest.fixture(scope="module")
def test_client():
    app = create_app("testing")

    # Execute sql file
    # Source: https://stackoverflow.com/questions/54289555/how-do-i-execute-an-sqlite-script-from-within-python


    with app.test_client() as test_client:
        with open('app/db/schema.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        db = sqlite3.connect(path)
        cursor = db.cursor()
        cursor.executescript(sql_script)
        db.commit()
        cursor.execute("INSERT INTO user (email, password) VALUES ('123@hotmail.com', 'cat')")
        db.commit()
        db.close()

        yield test_client

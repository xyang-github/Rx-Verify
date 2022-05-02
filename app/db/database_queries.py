import sqlite3

# Paths for the two database files: one for testing, and the other for deployment
path = "app/db/test.db"
# path = "app/db/db.db"


def query_select(query, key):
    """Send a select query and return the results"""
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(query, (key,))
    result = cur.fetchall()
    con.close()
    return result


def query_change(query, key):
    """Send a query to update, delete or insert the database"""
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(query, key)
    con.commit()
    con.close()


# Source: https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def query_medication_results(query, key):
    """Will send a select query to the database and return the result as a dictionary"""
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(query, key)
    result = cur.fetchall()
    con.close()
    return result


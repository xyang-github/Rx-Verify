import sqlite3

path = "app/db/db.db"


def query_select(query, key):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(query, (key,))
    result = cur.fetchall()
    con.close()
    return result


def query_change(query, key):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(query, key)
    con.commit()
    con.close()


# Source: https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def query_medication_results(query, key):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(query, key)
    result = cur.fetchall()
    con.close()
    return result


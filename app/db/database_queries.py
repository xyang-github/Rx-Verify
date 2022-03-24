import sqlite3
path = "app/db/db.db"


def query_select(query, key):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(query, (key,))
    result = cur.fetchall()
    con.close()
    return result


def query_change(query):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    con.close()
    return result
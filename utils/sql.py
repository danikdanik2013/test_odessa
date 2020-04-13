import sqlite3

from config import DB_NAME


def connect_to_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS allo(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, link text, varification text, counter INTEGER )"
    )
    return cur, conn

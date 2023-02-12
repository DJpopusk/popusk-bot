import sqlite3

con = sqlite3.connect("allDATA.db")
cur = con.cursor()
try:
    res = cur.execute("SELECT * From message").fetchall()
except:
    cur.execute("""CREATE TABLE message (
    id       INTEGER PRIMARY KEY AUTOINCREMENT
                     UNIQUE
                     NOT NULL,
    If_dm    BOOLEAN NOT NULL,
    user_id  STRING NOT NULL,
    sever_id INTEGER
    );
    """)
    cur.execute("""CREATE TABLE message_data (
    message_id         NOT NULL
                       UNIQUE
                       PRIMARY KEY,
    data_type  BOOLEAN NOT NULL,
    text       TEXT,
    time       TIME,
    date       DATE
    );
    """)
    cur.execute("""CREATE TABLE id_to_name (
    id   INTEGER PRIMARY KEY
                 NOT NULL,
    name TEXT    NOT NULL
    );
    """)
con.commit()

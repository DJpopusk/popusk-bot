import sqlite3


def setup():
    con = sqlite3.connect("allDATA.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE message (
    id    INTEGER PRIMARY KEY AUTOINCREMENT
                  UNIQUE
                  NOT NULL,
    text  STRING,
    ch_id INTEGER,
    m_id  INTEGER,
    s_id  INTEGER,
    time  TIME,
    date  DATE,
    attachment STRING
 );

    """)
    cur.execute("""CREATE TABLE channels (
    id    INTEGER PRIMARY KEY AUTOINCREMENT
                  UNIQUE
                  NOT NULL,
    ch_id INTEGER,
    title STRING
);
""")
    cur.execute("""CREATE TABLE servers (
    id    INTEGER NOT NULL
                  UNIQUE
                  PRIMARY KEY AUTOINCREMENT,
    s_id  INTEGER,
    title STRING
);
""")
    con.commit()

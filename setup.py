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
    server_id INTEGER
    );
    """)
    cur.execute("""CREATE TABLE message_data (
    
    id     INTEGER UNIQUE
                   PRIMARY KEY AUTOINCREMENT
                   NOT NULL,
    data_type  BOOLEAN NOT NULL,
    text       TEXT,
    time       TIME,
    date       DATE
    message_id         NOT NULL
                       UNIQUE
                       PRIMARY KEY
    );
    """)
    cur.execute("""CREATE TABLE id_to_name (
    id     INTEGER UNIQUE
                   PRIMARY KEY AUTOINCREMENT
                   NOT NULL,,
    name TEXT    NOT NULL
    );
    """)
    cur.execute("""CREATE TABLE users (
    id     INTEGER UNIQUE
                   PRIMARY KEY AUTOINCREMENT
                   NOT NULL,,
    user STRING  NOT NULL
                 UNIQUE,
    type INTEGER DEFAULT (0) 
    );
    """)
    cur.execute("""CREATE TABLE channels (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name   STRING,
    c_id   INTEGER,
    server INTEGER
    );
      """)
con.commit()

import sqlite3


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn, create_table):
    c = conn.cursor()
    c.execute(create_table)


def setup():
    db = "all_data.db"
    create = """CREATE TABLE message (
    id       INTEGER PRIMARY KEY AUTOINCREMENT
                     UNIQUE
                     NOT NULL,
    If_dm    BOOLEAN NOT NULL,
    user_id  INTEGER NOT NULL,
    sever_id INTEGER
    );
    """
    create2 = """CREATE TABLE message_data (
    message_id         NOT NULL
                       UNIQUE
                       PRIMARY KEY,
    data_type  BOOLEAN NOT NULL,
    text       TEXT,
    time       TIME,
    date       DATE
    );
    """
    create3 = """CREATE TABLE id_to_name (
    id   INTEGER PRIMARY KEY
                 NOT NULL,
    name TEXT    NOT NULL
    );
    """
    conn = create_connection(db)
    create_table(conn, create)
    create_table(conn, create2)
    create_table(conn, create3)


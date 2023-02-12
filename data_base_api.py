import sqlite3


def add_message(message_data, author, channel=None, date=None, time=None):
    con = sqlite3.connect("allDATA.db")
    cur = con.cursor()
    cur.execute("INSERT INTO message (if_dm, user_id)"
                f"VALUES (False, '{author}')")
    cur.execute("""""")
    con.commit()

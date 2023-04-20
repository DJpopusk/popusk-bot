import sqlite3
import datetime


def url_decode(url):
    if not url:
        return dict()
    ur1 = url.replace("//", "/")
    ur1 = url.split("/")
    values = ur1[3:]
    keys = ["type", "server", "channel", "message"]
    return dict(zip(keys, values))


def add_message(message):
    timing = message.created_at
    url = message.jump_url
    attachments = message.attachments

    data = message.content
    tm = datetime.time(timing.hour, timing.minute, timing.second)
    dt = datetime.date(timing.year, timing.month, timing.day)
    encoded = url_decode(url)
    con = sqlite3.connect("allDATA.db")
    cur = con.cursor()
    time = tm.strftime("%H-%M-%S")
    date = dt.strftime("%Y-%m-%d")
    m = encoded["message"]
    s = encoded["server"]
    print(attachments)
    if attachments:
        print("123")
        cur.execute(
            f"""INSERT INTO message (text, ch_id, m_id, s_id, time, date, attachment)
             VALUES ('{data}', {message.channel.id}, {m}, {s}, {time}, {date}, '{attachments[0].url}')""")
    else:
        cur.execute(
            f"""INSERT INTO message (text, ch_id, m_id, s_id, time, date)
             VALUES ('{data}', {message.channel.id}, {m}, {s}, '{time}', '{date}')""")
    channels = cur.execute("""SELECT ch_id FROM channels;""").fetchall()
    if message.channel != "Direct Message with Unknown User" and message.channel.id not in channels:
        cur.execute(f"""INSERT INTO channels (ch_id, title) VALUES ({message.channel.id}, '{message.channel}');""")
    con.commit()

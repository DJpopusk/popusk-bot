# import sqlite3
#
#
# def add_message(message_data, author, channel=None, time=None, url=None):
#     """adds info about message and adds data to message data
#     ::param message_data: message data
#     ::param author: author of message
#     ::param channel: channel
#     ::param date: date of message
#     ::param time: time of message
#     ::param url: url of message"""
#     print(message_data, author, channel, time, url)
#     con = sqlite3.connect("allDATA.db")
#     cur = con.cursor()
#     data = url_decode(url)
#
#     if_dm = False
#     print(data)
#     if data["server"] == "@me":
#         if_dm = True
#     cur.execute(f"""INSERT INTO message (if_dm, user_id, server_id, channel, message_id)
#          VALUES ({if_dm}, '{author}', {data['server']}, {data['channel']}, {data['message']})""")
#     # cur.execute("""INSERT INTO message_data (data_type, text, time, date, message_id)""")
#
#     # chans = cur.execute("""SELECT c_id FROM channels""").fetchall()
#     # if data["channel"] not in chans:
#     #     add_channel(channel, data)
#     con.commit()
#
#
# def add_channel(name, url):
#     """adds a channel to the database
#     ::param name - the name of the channel user sees
#     ::param url - url to encode"""
#     con = sqlite3.connect("allDATA.db")
#     cur = con.cursor()
#     data = url
#     print(data['channel'], name, data['server'])
#     data = [url["channel"], url["server"]]
#     cur.execute(f"""INSERT INTO channels (name, c_id, server) VALUES ('{name}',{data[0]} ,{data[1]} )""")
#     con.commit()
#
#
# def url_decode(url):
#     ur1 = url.replace("//", "/")
#     ur1 = url.split("/")
#     values = ur1[3:]
#     keys = ["type", "server", "channel", "message"]
#     return dict(zip(keys, values))
#
#
# def add_message_data(m_id, data, date, time):
#     """::param m_id: ID of the message
#     ::param data: message data
#     ::param date: date of messagex
#     ::param time: time of message"""
#
#     con = sqlite3.connect("allDATA.db")
#     cur = con.cursor()
#     cur.execute("""INSERT INTO message_data (data_type, text, time, date, message_id)
#     VALUES (?, ?,?,?,?,?)""", (data[0], data[1], time, date, m_id))
#     con.commit()


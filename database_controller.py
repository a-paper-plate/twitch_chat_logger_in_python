import os
import sqlite3
from datetime import datetime
current_dir=os.path.dirname(os.path.abspath(__file__))
if os.path.exists(f"{current_dir}\\logs.db"):
    conn = sqlite3.connect(f"{current_dir}\\logs.db", check_same_thread=False)
    cur = conn.cursor()
else:
    conn = sqlite3.connect(f"{current_dir}\\logs.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE chat_db (
                time text,
                streamer text,
                user text,
                msg text
                )""")
    cur.execute("""CREATE TABLE streamers_db (
                        streamers text,
                        message_count INTEGER 
                        )""")

    cur.execute("""CREATE TABLE users_db (
                        messenger text,
                        message_count INTEGER  
                        )""")
    conn.commit()
def add_error(e,error,cwd):
    with open(f"{cwd}/errors.txt","a+", encoding="utf-8") as file:
        file.write(f"\n[{e}]["+str(datetime.now())+"]"+error)
    file.close()
def add_message(msg_time,streamer_name,sender_name,msg):
    cur.execute(f"INSERT INTO chat_db VALUES (?,?,?,?)",(msg_time,streamer_name,sender_name,msg))
    cur.execute(f"""SELECT message_count FROM streamers_db WHERE streamers=?;""", [streamer_name])
    result = cur.fetchone()
    if result:
        cur.execute(f"""Update streamers_db set message_count ={int(result[0])+1} WHERE streamers=?;""", [streamer_name])
    else:
        cur.execute("INSERT INTO streamers_db VALUES (?,?)", [streamer_name,1])
    cur.execute(f"""SELECT message_count FROM users_db WHERE messenger=?;""", [sender_name])
    result = cur.fetchone()
    if result:
        cur.execute(f"""Update users_db set message_count ={int(result[0])+1} WHERE messenger=?;""", [sender_name])
    else:
        cur.execute("INSERT INTO users_db VALUES (?,?)", [sender_name,1])
    conn.commit() 
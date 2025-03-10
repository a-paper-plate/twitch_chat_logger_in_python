import sqlite3
import os
import re
import matplotlib.pyplot as plt

sting=".*gay.*"




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
def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None
conn.create_function("REGEXP", 2, regexp)
cur.execute(f"""SELECT time FROM chat_db WHERE msg REGEXP ?;""", [sting])
result = cur.fetchall()
print(len(result))
final_list={}

for msg_time in result:
    msg_time=msg_time[0]
    msg_time=msg_time.split(" ")[0]
    if msg_time in final_list:
        final_list[msg_time] += 1
    else:
        final_list[msg_time] = 1
time_list=[]
int_list=[]
for i in final_list.items():
    time_list.append(i[0])
    int_list.append(i[1])
plt.plot(time_list, int_list)
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title(sting)
plt.show()
print(final_list)
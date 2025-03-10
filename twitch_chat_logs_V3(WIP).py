from multiprocessing import Process,Pipe
import threading
import select
import socket
import datetime
import requests
import re
import os
import sqlite3
import time
def start_database(log_file_name:str="Log"):
    current_dir=os.path.dirname(os.path.abspath(__file__))
    if os.path.exists(f"{current_dir}\\{log_file_name}.db"):
        database_connection = sqlite3.connect(f"{current_dir}\\{log_file_name}.db", check_same_thread=False)
        database_cursor = database_connection.cursor()
    else:
        database_connection = sqlite3.connect(f"{current_dir}\\{log_file_name}.db", check_same_thread=False)
        database_cursor = database_connection.cursor()
        database_cursor.execute("""CREATE TABLE chat_db (
                    streamer text,
                    user text,
                    user_id text,
                    first_msg text,
                    color text,
                    time text,
                    msg text
                    )""")
        database_cursor.execute("""CREATE TABLE streamers_db (
                    streamers text,
                    message_count INTEGER 
                    )""")

        database_cursor.execute("""CREATE TABLE users_db (
                    messenger text,
                    message_count INTEGER  
                    )""")
        database_connection.commit()
    return database_connection,database_cursor





def database_add_message(database_connection,database_cursor,msg_data):
    database_cursor.execute(f"INSERT INTO chat_db VALUES (?,?,?,?,?,?,?)",(msg_data["streamer_name"],msg_data["message_sender"],msg_data["user-id"],msg_data["first-msg"],msg_data["color"],msg_data["tmi-sent-ts"],msg_data["message"],))
    database_cursor.execute(f"""SELECT message_count FROM streamers_db WHERE streamers=?;""", [msg_data["streamer_name"]])
    result = database_cursor.fetchone()
    if result:
        database_cursor.execute(f"""Update streamers_db set message_count ={int(result[0])+1} WHERE streamers=?;""", [msg_data["streamer_name"]])
    else:
        database_cursor.execute("INSERT INTO streamers_db VALUES (?,?)", [msg_data["streamer_name"],1])
    database_cursor.execute(f"""SELECT message_count FROM users_db WHERE messenger=?;""", [msg_data["message_sender"]])
    result = database_cursor.fetchone()
    if result:
        database_cursor.execute(f"""Update users_db set message_count ={int(result[0])+1} WHERE messenger=?;""", [msg_data["message_sender"]])
    else:
        database_cursor.execute("INSERT INTO users_db VALUES (?,?)", [msg_data["message_sender"],1])
    database_connection.commit()



def connect_to_streamer(streamer_username,socket_to_connect_with)->None:
	socket_to_connect_with.send(bytes(f"JOIN #{streamer_username}\r\n", "UTF-8"))
	connection_test_message=socket_to_connect_with.recv(1024).decode('utf8')
	if connection_test_message[:21]==":tmi.twitch.tv NOTICE":
		return None
	return 1








def format_message_data(nonformatted_message:str)->dict:
    #(message metadata) (message sender) (streamer name) (message)
    temporary_data_dictionary={}
    try:
        message_data=re.split(R"@([^ ]+) :([^!]+)![^ ]+ PRIVMSG #([^ ]+) :(.+)\\r\\n",nonformatted_message)
    
        message_data.pop(0)
        message_data.pop(-1)
        
        
        nonformatted_message_data=message_data[0].split(";",16)
        for data in nonformatted_message_data:
            data=data.split("=")
            try:
                temporary_data_dictionary[data[0]]=data[1]
            except:
                temporary_data_dictionary[data[0]]=""
        temporary_data_dictionary["message_sender"]=message_data[1]
        temporary_data_dictionary["streamer_name"]=message_data[2]
        temporary_data_dictionary["message"]=message_data[3]
        print(temporary_data_dictionary)
    except Exception as e :
        temporary_data_dictionary["user-id"]="error"
        temporary_data_dictionary["first-msg"]="error"
        temporary_data_dictionary["color"]="error"
        temporary_data_dictionary["tmi-sent-ts"]="error"
        temporary_data_dictionary["message_sender"]="error"
        temporary_data_dictionary["streamer_name"]="error"
        temporary_data_dictionary["message"]="error"
        print(e)
    return temporary_data_dictionary
        
    





def convert_timestamp_to_readable_time(timestamp):
	timestamp_int = float(timestamp)
	datetime_object = datetime.datetime.fromtimestamp(timestamp_int/1000)
	return datetime_object.strftime('%Y-%m-%d %H:%M:%S')



def message_data_cleansing(message_queue_pipe)->None:
    database_connection,database_cursor=start_database("Logs_V3")
    full_messages_list=[]
    message_queue=""
    
    while True:
        message_queue+=str(message_queue_pipe.recv())
        print("message_queue:"+str(message_queue))
        full_messages_list=re.findall("(@.+:.+!.+#.+ :.+\\r\\n)",message_queue)
        message_queue=""
        for msg in full_messages_list:
            message_queue+=str(re.sub(f"{msg}","",message_queue))
        print(message_queue)
        for message in full_messages_list:
            message_formatted=format_message_data(message)
            database_add_message(database_connection,database_cursor,message_formatted)



def get_top_X_streamers(client_id:str,token:str,X_number_of_streamers:int=10):
    current_top_X_streamers_of_the_hour=[]
    print(f":--------start-get_top_X_streamers-------:")
    api_response = requests.get("https://api.twitch.tv/helix/streams", params={"first": X_number_of_streamers}, headers={"Client-ID": client_id,"Authorization": f"Bearer {token}"})
    api_data = api_response.json()
    if "data" in api_data:
        top_streams = api_data["data"]
        for i, stream in enumerate(top_streams, start=1):
            print(str(i)+":"+str(stream['user_name']))
            current_top_X_streamers_of_the_hour.append(stream['user_name'])
        print(f":---------end-get_top_X_streamers--------:")
        return current_top_X_streamers_of_the_hour
    else:
        print(f"error getting top {X_number_of_streamers} streamers:{api_data}")
        print(f":---------end-get_top_X_streamers--------:")
        return current_top_X_streamers_of_the_hour



def separate_list(input_list, filter_list):
    in_filter_list = []
    not_in_filter_list = []
    for item in input_list:
        if item in filter_list:
            in_filter_list.append(item)
        else:
            not_in_filter_list.append(item)
    return in_filter_list, not_in_filter_list


def keep_channels_updated(client_id,token,user_selected_streamers,socket_connection):
    global full_streamer_list

    while True:
        time.sleep(2800)
        new_top_X_streamer_list=get_top_X_streamers(client_id,token,10)
        full_streamer_list= user_selected_streamers+new_top_X_streamer_list
        keep,disconnect =separate_list(active_top_X_streamer_list, new_top_X_streamer_list)
        _,channels_to_connect =separate_list(new_top_X_streamer_list, keep)
        for channel_name in disconnect:
            socket_connection.send(bytes("PART #" + channel_name + "\r\n", "UTF-8"))
        for channel_name in channels_to_connect:
            socket_connection.send(bytes(f"JOIN #{streamer_username}\r\n", "UTF-8"))
            socket_connection.recv(1024).decode('utf8')



if __name__ == "__main__":
    nick_name = "a_paper_plate__chat_logger_testing"
    client_id = "5pfc0x3g6vl810o6begg2h8ue9xj6v"
    client_secret = "pfc6uoaygy5rv17cqrgoxtncm6odx4"
    token = "uq5fc8mirk29cov2o7z98o172mb5oh"
    pipe_in,pipe_out=Pipe(False)
    t=Process(target=message_data_cleansing,args=(pipe_in,))
    t.start()
    user_selected_streamers=input("channels to log separated by a comma(,) up to 10:")
    if len(user_selected_streamers)>=1:
        user_selected_streamers=user_selected_streamers.split(",")
    else:
        user_selected_streamers=[]
    active_top_X_streamer_list=get_top_X_streamers(client_id,token,10)
    full_streamer_list=user_selected_streamers+active_top_X_streamer_list
    socket_connection = socket.socket()
    socket_connection.connect(("irc.chat.twitch.tv", 6667))
    socket_connection.send(bytes(f"PASS oauth:{token}\r\nNICK {nick_name}\r\nCAP REQ :twitch.tv/tags twitch.tv/tags \r\n", "UTF-8"))
    socket_connection.recv(1024).decode('utf8')
    connected_channels_list=[socket_connection]
    for streamer_username in full_streamer_list:
        socket_connection.send(bytes(f"JOIN #{streamer_username}\r\n", "UTF-8"))
        socket_connection.recv(1024).decode('utf8')
    threading.Thread(target=keep_channels_updated, args=(client_id,token,user_selected_streamers,socket_connection)).start()

    while True:
        readable, _, _ = select.select(connected_channels_list, [],[])
        for channel in readable:

            incoming_message=channel.recv(1028).decode('utf8')
            if incoming_message[:3]=="PING":
                channel.send("PONG")
                continue
            else:
                pipe_out.send(incoming_message)
"""ivycomb"""


			
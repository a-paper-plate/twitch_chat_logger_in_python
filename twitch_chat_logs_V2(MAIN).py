import socket
import select
import threading
import requests
import time

NICK = "paper_chat_loger"
client_id = "5pfc0x3g6vl810o6begg2h8ue9xj6v"
client_secret = "pfc6uoaygy5rv17cqrgoxtncm6odx4"
token = 'uq5fc8mirk29cov2o7z98o172mb5oh'
dictionary={}
user_sockets=[]
nonformatted_message_queue=[]
active_top_X_streamer_list=[]
paused=False

def create_sockets(user_list):
    print(":----start-create_sockets-----:")
    final_socket_list = []
    for i in user_list:
        if len(i)>=1:
            s = socket.socket()
            s.connect(("irc.chat.twitch.tv", 6667))
            s.send(bytes("PASS oauth:" + token + "\r\n", "UTF-8"))
            s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
            s.send(bytes("JOIN #" + i + " \r\n", "UTF-8"))
            s.send(bytes("CAP REQ :twitch.tv/tags twitch.tv/tags \r\n", "UTF-8"))
            s.setblocking(1)
            temp=s.recv(1024).decode('utf8')
            if ":tmi.twitch.tv NOTICE" == temp[0:20]:
                print(f"failed to connect to channel\nerror:{temp[25:]}")
            print(f"successfully connected to {i}!")
            s.setblocking(False)
            final_socket_list.append(s)
            dictionary[str(i)]=s
    print(":----end-create_sockets-----:")
    return final_socket_list



def disconnect_from_selected_channels(users_to_disconnect):
    global user_sockets
    print(":----start-disconnect_from_selected_channels-----:")
    for channel_name in users_to_disconnect:
        for i in user_sockets[:]:
            if i==dictionary[str(channel_name)]:
                user_sockets.remove(i)
        dictionary[str(channel_name)].send(bytes("PART #" + channel_name + "\r\n", "UTF-8"))
        dictionary[str(channel_name)].close()
        del dictionary[str(channel_name)]
        print("successfully removed "+str(channel_name))
    print(":----end-disconnect_from_selected_channels-----:")

def separate_list(input_list, filter_list):
    in_filter_list = []
    not_in_filter_list = []
    for item in input_list:
        if item in filter_list:
            in_filter_list.append(item)
        else:
            not_in_filter_list.append(item)
    return in_filter_list, not_in_filter_list

def get_top_X_streamers(client_id,token,X_number_of_streamers):
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
    


def keep_channels_updated(client_id,token,user_selected_streamers,full_streamer_list):
    global paused
    global user_sockets
    global active_top_X_streamer_list
    global nonformatted_message_queue
    while True:
        time.sleep(2800)
        paused=True
        
        print(":--------start-keep_channels_updated-------:")
        print("paused the message logger")
        print("current messages in queue: "+str(len(nonformatted_message_queue)))
        new_top_X_streamer_list=get_top_X_streamers(client_id,token,10)
        full_streamer_list= user_selected_streamers+new_top_X_streamer_list
        keep,disconnect =separate_list(active_top_X_streamer_list, new_top_X_streamer_list)
        _,channels_to_connect =separate_list(new_top_X_streamer_list, keep)
        active_top_X_streamer_list=[]
        active_top_X_streamer_list=keep
        active_top_X_streamer_list.extend(channels_to_connect)
        disconnect_from_selected_channels(disconnect)
        
        temp=create_sockets(channels_to_connect)
        user_sockets.extend(temp)
        print("current messages in queue: "+str(len(nonformatted_message_queue)))
        print("unpaused the message logger")
        print(":---------end-keep_channels_updated--------:")
        paused=False
        



def format_data(nonformatted_data):
    temp_data={}
    nonformatted_data=nonformatted_data.split(";")
    for i in nonformatted_data:
        i=i.split("=")
        try:
            temp_data[i[0]]=i[1]
        except:
            temp_data[i[0]]=""
    return temp_data



def format_messagees(dictionary):
    global nonformatted_message_queue
    from datetime import datetime
    import database_controller
    import inspect
    cwd = inspect.getfile(lambda: None).rsplit('\\', 1)[0]

    while True:
        try:
            if not paused:
                if len(nonformatted_message_queue) >0:
                    nonformatted_msg_data_and_msg=nonformatted_message_queue.pop(0)
                    nonformatted_msg_data,temp=nonformatted_msg_data_and_msg.split("user-type=")
                    msg_data=format_data(nonformatted_msg_data)
                    temp=temp.split("#")
                    msg_data["streamer_name"],msg_data["msg"]=temp[1].split(" :")
                    if str(msg_data["msg"])=="!ping":
                        print("pong")
                        print(msg_data["streamer_name"])
                        print(dictionary)
                        print(dictionary[str(msg_data["streamer_name"])])
                        dictionary[str(msg_data["streamer_name"])].send(f"PRIVMSG #{msg_data['streamer_name']} :pong!\r\n0".encode('utf-8'))
                        print("ending")
                    print("\033[1;33;40m"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" \033[1;31;40m"+msg_data["streamer_name"]+"\033[1;32;40m"+msg_data["display-name"]+"\033[0m:\033[1;34;40m"+msg_data["msg"]+"\033[0m")
                    database_controller.add_message(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),msg_data["streamer_name"],msg_data["display-name"],msg_data["msg"])
        except Exception as error:
            database_controller.add_error(error,nonformatted_msg_data_and_msg,cwd)






def main():
    global active_top_X_streamer_list
    global user_sockets
    user_selected_streamers=input("channels to log separated by a comma(,) up to 10:")
    user_selected_streamers=user_selected_streamers.split(",")


    active_top_X_streamer_list=get_top_X_streamers(client_id,token,10)
    full_streamer_list=user_selected_streamers+active_top_X_streamer_list
    user_sockets = create_sockets(full_streamer_list)
    threading.Thread(target=format_messagees, args=(dictionary,)).start()
    threading.Thread(target=keep_channels_updated, args=(client_id,token,user_selected_streamers,full_streamer_list)).start()
    while True:
        readable, _, _ = select.select(user_sockets, [],[])
        if len(readable) != 0:
            for channel in readable:
                try:
                    nonformatted_message=str(channel.recv(1024).decode('utf8',errors='replace'))
                except Exception as error:
                    if channel.fileno()==-1:
                        pass
                        nonformatted_message="\r\n"
                    else:
                        error_file=open("./code_error.txt","w")
                        error_file.write(str(error)+"\nuser_sockets:"+str(user_sockets)+"\nchannel:"+str(channel)+"\nreadable:"+str(readable))
                        error_file.close()
                        print(error)
                        exit(2)
                if str(nonformatted_message).startswith('PING'):
                    channel.send("PONG\n".encode('utf-8'))
                else:
                    nonformatted_message=nonformatted_message.rstrip().split("\r\n")
                    for i in nonformatted_message:
                        nonformatted_message_queue.append(i)




if __name__ == "__main__":
    main()
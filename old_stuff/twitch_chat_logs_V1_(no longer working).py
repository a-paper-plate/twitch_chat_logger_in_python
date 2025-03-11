import socket
import select
import threading
import requests
import time
NICK = "paper_chat_loger"
client_id = "5pfc0x3g6vl810o6begg2h8ue9xj6v"
client_secret = "pfc6uoaygy5rv17cqrgoxtncm6odx4"
token = ""
dictionary={}
user_sockets=""
nonformatted_message_queue=[]





def get_top_10_streamers(client_id,token):
    current_top_10_streamers_of_the_hour=[]
    print("get_top_10_streamers")
    api_url = "https://api.twitch.tv/helix/streams"
    api_response = requests.get(api_url, params={"first": 5}, headers={"Client-ID": client_id,"Authorization": f"Bearer {token}"})
    api_data = api_response.json()
    if "data" in api_data:
        top_streams = api_data["data"]
        for _, stream in enumerate(top_streams, start=1):
            print(stream['user_name'])
            current_top_10_streamers_of_the_hour.append(stream['user_name'])
        print("get_top_10_streamers")
        return(current_top_10_streamers_of_the_hour)
    else:
        print("get_top_10_streamers")
        return(current_top_10_streamers_of_the_hour)





def disconnect_from_selected_channels(users_to_disconnect):
    for i,channel_socket in enumerate(users_to_disconnect):
        channel_socket.send(bytes("PART #" + dictionary[str(users_to_disconnect[i])] + "\r\n", "UTF-8"))
        channel_socket.close()
        del dictionary[str(users_to_disconnect[i])]
        users_to_disconnect.remove(users_to_disconnect [1])





def create_sockets(user_list):
    final_socket_list = []
    for index in range(0, len(user_list)):
        s = socket.socket()
        s.connect(("irc.chat.twitch.tv", 6667))
        s.setblocking(False)
        print(token)
        s.send(bytes("PASS oauth:" + token + "\r\n", "UTF-8"))
        s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
        s.send(bytes("JOIN #" + user_list[index] + " \r\n", "UTF-8"))
        s.send(bytes("CAP REQ :twitch.tv/tags twitch.tv/tags \r\n", "UTF-8"))
        final_socket_list.append(s)
        dictionary[str(user_list[index])]=s
    return final_socket_list





def keep_channels_updated(client_id,token,user_selected_streamers):
    global user_sockets
    while True:
        time.sleep(3600)
        top_10_streamers=get_top_10_streamers(client_id,token)
        full_streamer_list= top_10_streamers+user_selected_streamers
        disconnect_from_selected_channels(user_sockets,top_10_streamers)
        user_sockets=create_sockets(full_streamer_list)





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
    from cleantext import clean
    import os
    cwd = os.path.dirname(os.path.realpath(__file__))
    while True:
        try:
            if len(nonformatted_message_queue) >0:
                nonformatted_msg_data_and_msg=nonformatted_message_queue.pop(0)
                if len(nonformatted_msg_data_and_msg) >10:
                    nonformatted_msg_data,temp=clean(nonformatted_msg_data_and_msg, no_emoji=True).split("user-type=")
                    msg_data=format_data(nonformatted_msg_data)
                    temp=temp.split("#")
                    msg_data["streamer_name"],msg_data["msg"]=temp[1].split(" :")
                    msg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    msg=msg_data["msg"].replace("'", '&#130').replace('"', '&#34').replace(':', '&#58').replace(';', '&#59').replace('=', '&#61').replace('*', '&#42')
                    if str(msg)=="!ping":
                        dictionary(msg_data["streamer_name"]).send(f"PRIVMSG #{msg_data['streamer_name']} :pong".encode('utf-8'))
                    database_controller.add_message(msg_time,msg_data["streamer_name"],msg_data["display-name"],msg)
        except Exception as error:
            database_controller.add_error(error,nonformatted_msg_data_and_msg,cwd)





def main():
    alive = True
    user_selected_streamers=input("channels to log separated by a comma(,) up to 10:")
    user_selected_streamers=user_selected_streamers.split(",")
    top_10_streamer_list=get_top_10_streamers(client_id,token)
    full_streamer_list=user_selected_streamers+top_10_streamer_list
    user_sockets = create_sockets(full_streamer_list)
    threading.Thread(target=format_messagees, args=(dictionary,)).start()
    threading.Thread(target=keep_channels_updated, args=(client_id,token,user_selected_streamers)).start()
    temp=0
    while alive:
        readable, _, _ = select.select(user_sockets, [],[])
        if len(readable) != 0:
            for channel in readable:
                nonformatted_message=str(channel.recv(1024).decode('utf8',errors="replace"))
                print(nonformatted_message)
                if str(nonformatted_message).startswith('PING'):
                    channel.send("PONG\n".encode('utf-8'))
                elif temp >len(full_streamer_list)*3:
                    nonformatted_message=nonformatted_message.rstrip().split("\r\n")
                    for i in nonformatted_message:
                        nonformatted_message_queue.append(i)
                else:
                    temp+=1





if __name__ == "__main__":
    response = requests.post('https://id.twitch.tv/oauth2/token', data={'client_id': client_id,'client_secret': client_secret,'grant_type': 'client_credentials'})

# Check if the request was successful
if response.status_code == 200:
    token_info = response.json()
    print(token_info)
    token = token_info['access_token']
    print(f'Access Token: {token}')
    main()
else:
    print(f'Failed to get access token. HTTP Status Code: {response.status_code}')
    
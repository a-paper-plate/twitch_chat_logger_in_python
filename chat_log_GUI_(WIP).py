import tkinter as tk
from tooltip import ToolTip







def display_chat_boxes(chats_in_a_row,chat_boxes):
    x=0
    y=1
    for chat_box in chat_boxes:
        chat_box[0].configure(width=chatbox_width,height=chatbox_height)
        chat_box[0].grid_forget()
        chat_box[0].grid(column=x,row=y, padx=10, pady=10)
        chat_box[1].place(x=0,y=chatbox_height-user_input_frame_height,width=chatbox_width)
        chat_box[1].update()
        chat_box[2].configure(width=int((chatbox_width-(user_input_padx*2)-7)/12))
        x=x+1
        if x==chats_in_a_row:
            x=0
            y=y+1

def update_chat_boxes(x,y) -> None:
    global chats_in_a_row
    if x:
        global chatbox_width
        chats_in_a_row=int(x)
        chatbox_width=window_width/chats_in_a_row-chatbox_padx*2
        display_chat_boxes(x,chat_boxes)
        return
    else:
        global chats_in_a_column_on_screen
        global chatbox_height
        chats_in_a_column_on_screen=int(y)
        chatbox_height=window_width/chats_in_a_column_on_screen-chatbox_pady*2

        display_chat_boxes(chats_in_a_row,chat_boxes)





window_height:int=800
window_width:int=800
window = tk.Tk()
window.geometry(f"{str(window_height)}x{str(window_width)}")
window.configure(bg='#20201d')
window.title("test")





loged_chats:list[str]=["chat 1","chat 2","chat 3","chat 4","chat 5","chat 6","chat 7","chat 8","chat 9"]
global chats_in_a_row
global chats_in_a_column_on_screen
global chatbox_width
global chatbox_height

chatbox_padx=10
chatbox_pady=10
user_input_padx=5
user_input_pady=3
user_input_frame_height=40
chats_in_a_row=3
chats_in_a_column_on_screen=2
chatbox_width=window_width/chats_in_a_row-chatbox_padx*2
chatbox_height=window_width/chats_in_a_column_on_screen-chatbox_pady*2




chat_boxes:list[tk.Frame]=[]

chat_box_sizes_frame=tk.Frame(master=window)
tk.Scale(chat_box_sizes_frame,orient="horizontal",showvalue=False,from_=1, to=5,command=lambda event:update_chat_boxes(event,None)).grid(column=0,row=0)
tk.Scale(chat_box_sizes_frame,orient="horizontal",showvalue=False,from_=1, to=3,command=lambda event:update_chat_boxes(None,event)).grid(column=1,row=0)
chat_box_sizes_frame.grid(row=0,column=0,columnspan=5,sticky="w")


for chat in loged_chats:
    chatbox=tk.Frame(master=window,name=chat,background="#18181b",width=chatbox_width,height=chatbox_height)
    ##18181b
    
    
    user_input=tk.Frame(master=chatbox,name=f"{chat}_user_input_frame",background="#111114",padx=user_input_padx,pady=user_input_pady)
    user_input.place(x=0,y=chatbox_height-user_input_frame_height,relwidth=chatbox_width)
    user_input.update()
    user_input_Entry=tk.Entry(master=user_input,bg="#18181b",width=int((chatbox_width-user_input_padx*2-7)/12),fg="#fff",font=("TkTextFont",13))
    user_input_Entry.grid(column=0,row=0)
    user_input_button=tk.Button(master=user_input,background="#9147ff",text="send",width=7)
    user_input_button.grid(column=1,row=0)
    


    chat_boxes.append((chatbox,user_input,user_input_Entry))

display_chat_boxes(chats_in_a_row,chat_boxes)


window.mainloop()

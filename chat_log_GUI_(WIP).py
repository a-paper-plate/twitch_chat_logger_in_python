import tkinter as tk
import tkinter.font as tkFont
from tooltip import ToolTip







def display_chat_boxes(chats_in_a_row,chat_boxes):
    x=0
    y=1
    for chat_box in chat_boxes:
        chat_box[0].grid_forget()
        chat_box[0].configure(width=chatbox_width,height=chatbox_height)
        chat_box[0].grid(column=x,row=y, padx=10, pady=10)
        chat_box[1].place(x=0,y=chatbox_height-user_input_frame_height,width=chatbox_width)
        user_input_Entry_width=chatbox_width-user_input_padx*4-width_of_send_button
        chat_box[2].configure(width=int((user_input_Entry_width)/char_width_px))
        x=x+1
        if x==chats_in_a_row:
            x=0
            y=y+1

def update_chat_boxes(x,y) -> None:
    
    if x:
        global chats_in_a_row
        global chatbox_width
        chats_in_a_row=int(x)
        chatbox_width=window_width/chats_in_a_row-chatbox_padx*2
    else:
        global chats_in_a_column_on_screen
        global chatbox_height
        chats_in_a_column_on_screen=int(y)
        chatbox_height=(window_height-first_row_height)/chats_in_a_column_on_screen-chatbox_pady*2

    display_chat_boxes(chats_in_a_row,chat_boxes)


def on_resize(event):
    if str(event.widget)!=".":
        return
    global window_height
    global window_width
    global chatbox_width
    global chatbox_height
    if (window_height==event.height) and (window_width==event.width):
        return
    
    window_height=event.height
    window_width=event.width
    chatbox_width=window_width/chats_in_a_row-chatbox_padx*2
    chatbox_height=(window_height-first_row_height)/chats_in_a_column_on_screen-chatbox_pady*2
    display_chat_boxes(chats_in_a_row,chat_boxes)


window_height:int=800
window_width:int=800
window = tk.Tk()
window.geometry(f"{str(window_height)}x{str(window_width)}")
window.configure(bg='#20201d')
window.title("test")





loged_chats:list[str]=[]
for i in range(100):
    loged_chats.append(f"chat {i}")
global chats_in_a_row
global chats_in_a_column_on_screen
global chatbox_width
global chatbox_height
char_width_px = tkFont.Font(family="TkTextFont", size=13).measure("a")
send_text_px = tkFont.Font(family="TkTextFont", size=12).measure("send")
width_of_send_button=send_text_px+10
first_row_height=20
chatbox_padx=10
chatbox_pady=10
user_input_padx=5
user_input_pady=3
user_input_frame_height=40
chats_in_a_row=3
chats_in_a_column_on_screen=1
chatbox_width=window_width/chats_in_a_row-chatbox_padx*2
chatbox_height=(window_height-first_row_height)/chats_in_a_column_on_screen-chatbox_pady*2






chat_box_sizes_frame=tk.Frame(master=window)
tk.Scale(chat_box_sizes_frame,orient="horizontal",showvalue=False,troughcolor="#000",activebackground="#111114",background="#18181b",from_=1, to=10,command=lambda event:update_chat_boxes(event,None)).grid(column=0,row=0)
tk.Scale(chat_box_sizes_frame,orient="horizontal",showvalue=False,troughcolor="#000",activebackground="#111114",background="#18181b",from_=1, to=10,command=lambda event:update_chat_boxes(None,event)).grid(column=1,row=0)

chat_box_sizes_frame.grid(row=0,column=0,columnspan=5,sticky="w")

chat_boxes:list[tk.Frame]=[]
for chat in loged_chats:
    chatbox=tk.Frame(master=window,name=chat,background="#18181b",width=chatbox_width,height=chatbox_height)
    
    
    
    user_input=tk.Frame(master=chatbox,name=f"{chat}_user_input_frame",background="#111114",padx=user_input_padx,pady=user_input_pady)
    user_input.place(x=0,y=chatbox_height-user_input_frame_height,relwidth=chatbox_width)
    
    user_input_Entry_width=float(80)*float(chatbox_width)/100
    user_input_button_width=chatbox_width-user_input_Entry_width
    user_input_Entry=tk.Entry(master=user_input,bg="#18181b",width=int((user_input_Entry_width-user_input_padx)/char_width_px),fg="#fff",font=("TkTextFont",13))
    user_input_Entry.grid(column=0,row=0,padx=user_input_padx,pady=user_input_pady)
    user_input_button=tk.Button(master=user_input,background="#9147ff",text="send",width=int((user_input_button_width-user_input_padx)/char_width_px))
    user_input_button.grid(column=1,row=0,padx=user_input_padx,pady=user_input_pady)
    


    chat_boxes.append((chatbox,user_input,user_input_Entry))

display_chat_boxes(chats_in_a_row,chat_boxes)


window.bind('<Configure>', on_resize)
window.mainloop()

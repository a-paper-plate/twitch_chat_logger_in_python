import tkinter as tk
import tkinter.font as tkFont
from tooltip import ToolTip



class GUI():
    def __init__(self,window,window_height:int=800,window_width:int=800):
        self.window=window
        self.window_height:int=window_height
        self.window_width:int=window_width
        self.char_width_px = tkFont.Font(family="TkTextFont", size=13).measure("a")
        self.send_text_px = tkFont.Font(family="TkTextFont", size=12).measure("send")
        self.width_of_send_button=self.send_text_px+10
        self.first_row_height:int=20
        self.chatbox_padx:int=10
        self.chatbox_pady:int=10
        self.user_input_padx:int=5
        self.user_input_pady:int=3
        self.user_input_frame_height:int=40
        self.chats_in_a_row:int=2
        self.chats_in_a_column_on_screen:int=1
        self.chatbox_width=self.window_width/self.chats_in_a_row-self.chatbox_padx*2
        self.chatbox_height=(self.window_height-self.first_row_height)/self.chats_in_a_column_on_screen-self.chatbox_pady*2
        self.user_input_Entry_width=float(80)*float(self.chatbox_width)/100
        self.user_input_button_width=self.chatbox_width-self.user_input_Entry_width
        self.chat_boxes:list[tk.Frame]=[]
        self.chat_box_sizes_frame=tk.Frame(master=window)
        tk.Scale(master=self.chat_box_sizes_frame,orient="horizontal",showvalue=False,troughcolor="#000",activebackground="#111114",background="#18181b",from_=1, to=10,command=lambda event:self.update_chat_box_table(event,None)).grid(column=0,row=0)
        tk.Scale(master=self.chat_box_sizes_frame,orient="horizontal",showvalue=False,troughcolor="#000",activebackground="#111114",background="#18181b",from_=1, to=10,command=lambda event:self.update_chat_box_table(None,event)).grid(column=1,row=0)
        self.chat_box_sizes_frame.grid(row=0,column=0,columnspan=5,sticky="w")
        self.window.bind('<Configure>', self.on_resize)



    def new_chat(self,chat_name):
        chatbox=tk.Frame(master=self.window,name=chat_name,background="#18181b",width=self.chatbox_width,height=self.chatbox_height)
        user_input=tk.Frame(master=chatbox,name=f"{chat_name}_user_input_frame",background="#111114",padx=self.user_input_padx,pady=self.user_input_pady)
        user_input.place(x=0,y=self.chatbox_height-self.user_input_frame_height,relwidth=self.chatbox_width)
        user_input_Entry=tk.Entry(master=user_input,bg="#18181b",width=int((self.user_input_Entry_width-self.user_input_padx)/self.char_width_px),fg="#fff",font=("TkTextFont",13))
        user_input_Entry.grid(column=0,row=0,padx=self.user_input_padx,pady=self.user_input_pady)
        tk.Button(master=user_input,background="#9147ff",text="send",width=int((self.user_input_button_width-self.user_input_padx)/self.char_width_px)).grid(column=1,row=0,padx=self.user_input_padx,pady=self.user_input_pady)

        self.chat_boxes.append((chatbox,user_input,user_input_Entry))


    def update_chat_box_display(self):
        x=0
        y=1
        for chat_box in self.chat_boxes:
            
            chat_box[0].configure(width=self.chatbox_width,height=self.chatbox_height)
            chat_box[1].place(x=0,y=self.chatbox_height-self.user_input_frame_height,width=self.chatbox_width)
            self.user_input_Entry_width=self.chatbox_width-self.user_input_padx*8-self.width_of_send_button
            chat_box[2].configure(width=int((self.user_input_Entry_width)/self.char_width_px))
            x=x+1
            if x==self.chats_in_a_row:
                x=0
                y=y+1

    
    def update_chat_box_grid(self):
        x=0
        y=1
        for chat_box in self.chat_boxes:
            chat_box[0].grid_forget()
            chat_box[0].grid(column=x,row=y, padx=10, pady=10)
            x=x+1
            if x==self.chats_in_a_row:
                x=0
                y=y+1
        self.update_chat_box_display()
        


    def on_resize(self,event):
        if str(event.widget)!=".":
            return
        if (self.window_height==event.height) and (self.window_width==event.width):
            return
        self.window_height=event.height
        self.window_width=event.width
        self.update_chat_box_size()
        



    def update_chat_box_size(self) -> None:
        self.chatbox_width=self.window_width/self.chats_in_a_row-self.chatbox_padx*2
        self.chatbox_height=(self.window_height-self.first_row_height)/self.chats_in_a_column_on_screen-self.chatbox_pady*2
        self.update_chat_box_display()
        


    def update_chat_box_table(self,chats_in_a_row:int|None=None,chats_in_a_column_on_screen:int|None=None) -> None:
        if chats_in_a_row:
            self.chats_in_a_row=int(chats_in_a_row)
        if chats_in_a_column_on_screen:
            self.chats_in_a_column_on_screen=int(chats_in_a_column_on_screen)
        self.update_chat_box_size()
        self.update_chat_box_grid()









window_height:int=800
window_width:int=800
window = tk.Tk()
window.geometry(f"{str(window_height)}x{str(window_width)}")
window.configure(bg='#20201d')
window.title("test")




the_gui=GUI(window,window_width=window_width,window_height=window_height)

for i in range(100):

    the_gui.new_chat(f"chat {i}")

the_gui.update_chat_box_grid()

window.mainloop()

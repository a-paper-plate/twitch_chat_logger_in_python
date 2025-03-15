import tkinter as tk
import tkinter.font as tkFont
from tooltip import ToolTip





class chat_box(tk.Frame):
    def __init__(self,master,height:int,width:int,chat_background:str,input_background:str,input_text_color:str,input_button_color:str,input_button_text:str,char_width_px:int):
        super().__init__(master,height=height,width=width)
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.width=width
        self.height=height

        self.user_input_padx:int=5
        self.user_input_pady:int=3

        self.get_user_input_widths=lambda width, split_percentage: [int(split_percentage)*int(width)/100, (int(100-split_percentage)*int(width)/100)]


        self.user_input_Entry_width,self.user_input_button_width=self.get_user_input_widths(self.width,80)
        self.char_width_px=char_width_px
        
        
        
        

        self.canvas = tk.Canvas(self,background=chat_background,border=0,borderwidth=0,highlightthickness=0)
        self.canvas.grid_propagate(False)
        self.canvas.grid(row=0, column=0, sticky="nsew")


        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)


        self.scrollable_frame = tk.Frame(master=self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.scrollable_frame.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        

        self.user_input_frame=tk.Frame(master=self,background=input_background,height=40,width=self.width,padx=self.user_input_padx,pady=self.user_input_pady)
        self.user_input_frame.grid_propagate(False)
        self.user_input_frame.grid(row=1,column=0,columnspan=2)

        self.user_input_Entry=tk.Entry(master=self.user_input_frame,bg=input_background,fg=input_text_color,width=int((self.user_input_Entry_width-self.user_input_padx*2)/self.char_width_px),font=("TkTextFont",13))
        self.user_input_Entry.grid(column=0,row=0,padx=self.user_input_padx,pady=self.user_input_pady)

        self.user_input_Button=tk.Button(master=self.user_input_frame,background=input_button_color,text=input_button_text,width=int((self.user_input_button_width-self.user_input_padx*2)/(self.char_width_px)),command=lambda: self.add_msg(self.user_input_Entry.get()))
        self.user_input_Button.grid(column=1,row=0,padx=self.user_input_padx,pady=self.user_input_pady)


    def update_size(self,new_width:int,new_height:int) -> None:
        self.width=new_width
        self.height=new_height
        self.user_input_Entry_width,self.user_input_button_width=self.get_user_input_widths(self.width,80)


        self.configure(width=self.width,height=self.height)
        self.user_input_frame.configure(width=self.width)
        self.user_input_Entry.configure(width=int((self.user_input_Entry_width-self.user_input_padx*2)/self.char_width_px))
        self.user_input_Button.configure(width=int((self.user_input_button_width-self.user_input_padx*2)/(self.char_width_px)))

        
    def add_msg(self,msg) -> None:
        
        msg_frame = tk.Frame(self.scrollable_frame)
        msg_frame.grid(row=1,column=0)

        tk.Label(msg_frame,text=msg).grid(row=0,column=0)
        tk.Button(msg_frame,text=msg,command=lambda:print(msg)).grid(row=0,column=1)












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
        self.user_input_frame_height:int=40
        self.chats_in_a_row:int=2
        self.chats_in_a_column_on_screen:int=2
        self.chatbox_width=self.window_width/self.chats_in_a_row-self.chatbox_padx*2
        self.chatbox_height=(self.window_height-self.first_row_height)/self.chats_in_a_column_on_screen-self.chatbox_pady*2
        self.user_input_Entry_width=float(80)*float(self.chatbox_width)/100
        self.user_input_button_width=self.chatbox_width-self.user_input_Entry_width
        self.chat_boxes:chat_box=[]
        self.chat_box_sizes_frame=tk.Frame(master=window)
        tk.Scale(master=self.chat_box_sizes_frame,orient="horizontal",showvalue=False,troughcolor="#000",activebackground="#111114",background="#18181b",from_=1, to=10,command=lambda event:self.update_chat_box_table(event,None)).grid(column=0,row=0)
        tk.Scale(master=self.chat_box_sizes_frame,orient="horizontal",showvalue=False,troughcolor="#000",activebackground="#111114",background="#18181b",from_=1, to=10,command=lambda event:self.update_chat_box_table(None,event)).grid(column=1,row=0)
        
        self.window.bind('<Configure>', self.on_resize)
        self.chat_box_sizes_frame.grid(row=0,column=0,columnspan=5,sticky="w")
        



    def new_chat(self,chat_name):
        temp_chat=chat_box(master=self.window,
        width=self.chatbox_width,
        height=self.chatbox_height,
        chat_background="#18181b",
        input_background="#111114",
        input_text_color="#fff",
        input_button_color="#9147ff",
        input_button_text="send",
        char_width_px=self.char_width_px)
        self.chat_boxes.append(temp_chat)


        """
        chatbox_frame=tk.Frame(master=self.window,name=chat_name,background="#18181b",width=self.chatbox_width,height=self.chatbox_height)
        user_input=tk.Frame(master=chatbox_frame,name=f"{chat_name}_user_input_frame",background="#111114",padx=self.user_input_padx,pady=self.user_input_pady)
        user_input.place(x=0,y=self.chatbox_height-self.user_input_frame_height,relwidth=self.chatbox_width)
        user_input_Entry=tk.Entry(master=user_input,bg="#18181b",width=int((self.user_input_Entry_width-self.user_input_padx)/self.char_width_px),fg="#fff",font=("TkTextFont",13))
        user_input_Entry.grid(column=0,row=0,padx=self.user_input_padx,pady=self.user_input_pady)
        tk.Button(master=user_input,background="#9147ff",text="send",width=int((self.user_input_button_width-self.user_input_padx)/self.char_width_px)).grid(column=1,row=0,padx=self.user_input_padx,pady=self.user_input_pady)

        self.chat_boxes.append((chatbox_frame,user_input,user_input_Entry))"""



    def update_chat_box_display(self):
        self.chatbox_width=int(self.window_width/self.chats_in_a_row-self.chatbox_padx*2)
        self.chatbox_height=int((self.window_height-self.first_row_height)/self.chats_in_a_column_on_screen-self.chatbox_pady*2)
        for the_chat_box in self.chat_boxes:
            the_chat_box.update_size(self.chatbox_width,self.chatbox_height)

    
    def update_chat_box_grid(self):
        x=0
        y=1
        for chat_box in self.chat_boxes:
            chat_box.grid(column=x,row=y, padx=10, pady=10)
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
        self.update_chat_box_display()
        

        


    def update_chat_box_table(self,chats_in_a_row:int|None=None,chats_in_a_column_on_screen:int|None=None) -> None:
        if chats_in_a_row:
            self.chats_in_a_row=int(chats_in_a_row)
        elif chats_in_a_column_on_screen:
            self.chats_in_a_column_on_screen=int(chats_in_a_column_on_screen)
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
the_gui.update_chat_box_table(the_gui.chats_in_a_row,the_gui.chats_in_a_column_on_screen)

window.mainloop()

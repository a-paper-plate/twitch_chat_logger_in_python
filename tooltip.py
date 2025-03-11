import tkinter as tk
class ToolTip:
    ...
class ToolTip:
    instances:ToolTip=[]
    def __init__(self,master,widget,tooltip_window:tk.Frame|None=None,generate_mouse_controls:bool=True, force_MB1_deletion:bool=False)-> tk.Frame|None:
        """will generate tkinter.Frame for the tooltip if not given one with the master being whatever you give for the ToolTip's master (notable for tooltip positioning)"""
        # this almost isn't necessary but it is used for moving the tool tip to the right position
        self.master=master


        # saves widget for later use
        self.widget = widget


        # will generate a frame if not given one otherwise we'll use the one that was passed in
        if tooltip_window==None:
            self.tooltip_container = tk.Frame(master,name="tooltip")
        else:
            self.tooltip_container=tooltip_window
        
        

        # appends this object to a list that is accessible by all other tooltips
        ToolTip.instances.append(self)

        # generates Mouse controls if not told to do otherwise
        if generate_mouse_controls:
            if not force_MB1_deletion:
                master.bind('<Button-1>', self._hide_tooltip,add="+")
            self.widget.bind('<Button-3>', self._show_tooltip,add="+")

        # makes sure the tooltip is shown above the object it's assigned to and will print any exception that it gets
        try:
            self.tooltip_container.lift(widget)
        except Exception as e:
            print("Exception:"+str(e))



    

    def is_widget_inside(self,widget, container)->bool:
        """Check if 'widget' is inside 'container' at any level, including if the 'widget' IS the 'container'"""
        # checks if the widget is the container and returns true otherwise it continues
        if widget==container:
            return True
        # Traverse up the widget hierarchy
        parent = widget.master
        while parent:  
            if parent == container:
                return True
            parent = parent.master

        # the widget is not the container or inside the container
        return False 


    # used for allowing input of a tooltip as the widget or as the master of other widgets
    def __call__(self):
        return self.tooltip_container
    def __eq__(self, other):
        if self.tooltip_container==other:
            return True
        return False
    def __getattr__(self, name):
        if name == "master":
            return self.tooltip_container.master  # Explicitly return the actual master
        return getattr(self.tooltip_container, name)
    #-----------------------------start of internal functions-----------------------------
    def _hide_tooltip(self,event) -> None:
        """internal function for hiding the tooltip"""
        if not self.is_widget_inside(event.widget,self.tooltip_container):
            self.hide_tooltip()


    def _show_tooltip(self, event) -> None:
        """internal function for rendering the tooltip"""
        relative_x = event.widget.winfo_rootx()-self.master.winfo_rootx()+event.x
        relative_y = event.widget.winfo_rooty()-self.master.winfo_rooty()+event.y
        self.show_tooltip(x=int(relative_x), y=int(relative_y))
    #-----------------------------end of internal functions-----------------------------




    def show_tooltip(self, x:int=0, y:int=0) -> None:
        """Enables rendering of the tooltip and moves it to the (X,Y) position relative to the widget the tooltip's container(frame) is assigned to"""
        self.tooltip_container.place(x=x, y=y)


    def hide_tooltip(self) -> None:
        """Disables rendering of this tooltip"""
        self.tooltip_container.place_forget()


    def hide_all_tooltips(self) -> None:
        """Disables rendering of all tooltips"""
        for tooltip in ToolTip.instances:
            tooltip.tooltip_window.place_forget()


    def bind(self,button,func,add="") -> None:
        """used for putting a tooltip on a tooltip (again I don't know why you would do this but it's here)"""
        self.tooltip_container.bind(button, func,add=add)
        
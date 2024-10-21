from tkinter import Tk
from tkinter.ttk import Frame, Button
from tkcalendar import Calendar

class PopUpWindow(Tk):

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.master.add_child_window(self)


    def destroy(self):
        try:
            self.master.remove.child_window()
        except:
            pass
        return super().destroy()
    


class DatePicker(PopUpWindow):

    def __init__(self, master):
        super().__init__(master=master)

        self.title("select date")
        self.calender_frame = Frame(self)
        self.calender = Calendar(master=self.calender_frame, selectmode="day")
        self.calender.pack()
        self.calender_frame.pack()
        self.pack_buttons()




    def pack_buttons(self):
        button_frame = Frame(self)
        Button(button_frame, text="today", command=self.click_today, padding=10).pack(side="left")
        Button(button_frame, text="selected date", command=self.click_date, padding=10).pack(side="left")
        Button(button_frame, text="Cancle", command=self.destroy, padding=10).pack(side="left")
        button_frame.pack(side="bottom")

    def click_today(self):
        pass

    def click_date(self):
        pass

        

from tkinter import Tk, StringVar
from tkinter.ttk import Frame, Button
from tkcalendar import Calendar
from datetime import date

class PopUpWindow(Tk):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.main_window.add_child_window(self)


    def destroy(self):
        try:
            self.main_window.remove.child_window()
        except:
            pass
        return super().destroy()
    


class DatePicker(PopUpWindow):

    def __init__(self, main_window):
        super().__init__(main_window=main_window)

        self.title("select date")
        self.calender = Calendar(master=self, selectmode="day")
        self.calender.pack()
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

        

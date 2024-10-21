from scr.analytics import Analytics
from scr.center_frame import CenterFrame
from scr.bottom_frame import BottomFrame
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    """
    """
    USABLE_FREQUENCIES = {"WEEKLY" : 7, "DAILY" : 1}
    SELECTABLE_VALUES = ("frequency", "current streak", "longest streak")
    SELECTABLE_FREQUENCIES = ("Daily", "Weekly", "All")

    def __init__(self):
        super().__init__()

        self.analytics = Analytics()

        self.geometry("800x400")
        self.title("Habit Tracking App")

        self.top_frame = self.get_top_frame().pack(side="top")
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.pack(side="bottom")
        self.center_frame = CenterFrame(self, Analytics.HABIT_LIST_TITLES, self.analytics.all_habits)
        self.center_frame.pack(side="top", fill="both")



      

    def get_top_frame(self):
        top_frame = ttk.Frame(self)
        title = ttk.Label(top_frame, text="Habit Tracking App")
        title.pack()
        return top_frame 
    
    def reload_center_frame(self, column_names, habit_list):
        self.center_frame.destroy()
        self.center_frame = CenterFrame(self, column_names, habit_list)
        self.center_frame.pack(side="top", fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()
import tkinter as tk
from tkinter import ttk
from scr.analytics import Analytics
from scr.center_frame import CenterFrame
from scr.bottom_frame import BottomFrame


class App(tk.Tk):
    """
    """
    USABLE_FREQUENCIES = {"DAILY" : 1, "WEEKLY" : 7}
    SELECTABLE_VALUES = ("frequency", "current streak", "longest streak")
    SELECTABLE_FREQUENCIES = ("Daily", "Weekly", "All")

    def __init__(self):
        super().__init__()

        self.analytics = Analytics()
        self.child_windows = []

        self.geometry("900x450")
        self.title("Habit Tracking App")

        self.top_frame = self.get_top_frame()
        self.top_frame.pack(side="top")
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.pack(side="bottom")
        self.center_frame = CenterFrame(self,
                                        Analytics.HABIT_LIST_TITLES, self.analytics.all_habits)
        self.center_frame.pack(side="top", fill="both")


    def destroy(self):
        try:
            for child in self.child_windows:
                child.destroy()
        except AttributeError as exc:
            raise AttributeError("Child window has no Attribute destroy") from exc
        return super().destroy()

    def add_child_window(self, child):
        self.child_windows.append(child)
        for button in self.bottom_frame.buttons:
            button.state(["disabled"])

    def remove_child_window(self,child):
        self.child_windows.remove(child)
        for button in self.bottom_frame.buttons:
            button.state(["!disabled"])


    def get_top_frame(self):
        top_frame = ttk.Frame(self)
        title = ttk.Label(top_frame, text="Habit Tracking App")
        title.pack()
        return top_frame

    def reload_center_frame(self, habit_list):
        self.center_frame.destroy()
        self.center_frame = CenterFrame(self, Analytics.HABIT_LIST_TITLES, habit_list)
        self.center_frame.pack(side="top", fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()

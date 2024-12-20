"""
NAME
    main

DESCRIPTION
    Excecute the habit tracking app

CLASSES
    tk.TK
        App
"""
import tkinter as tk
from tkinter import ttk
import scr.analytics as ana
from scr.habit import Habit
from scr.center_frame import CenterFrame
from scr.bottom_frame import BottomFrame


class App(tk.Tk):
    """
    The main application class for the Habit Tracking App.
    
    Attributes:
        USABLE_FREQUENCIES (dict): Implemented frequency keys:["DAILY"]=1 ,["WEEKLY"]=7
        SELECTABLE_FREQUENCIES (tuple): Selectable frequencies:
                                    ("Daily", "Weekly", "Selected", "All")
        HABIT_LIST_TITLES (tuple): ("selected", "habit name", "description", "frequency",
                         "current streak", "longest streak")
        
        all_habits (list): A of all habits which are saved in the database.
        child_windows (list): A list to keep track of child windows.
        top_frame (ttk.Frame): The top frame of the application.
        bottom_frame (BottomFrame): The bottom frame of the application.
        center_frame (CenterFrame): The center frame of the application displaying the habit data.
    """
    USABLE_FREQUENCIES = {"Daily" : 1, "Weekly" : 7}
    SELECTABLE_FREQUENCIES = ("Daily", "Weekly", "Selected", "All")
    HABIT_LIST_TITLES = ("selected", "habit name", "description", "frequency",
                         "current streak", "longest streak")


    def __init__(self):
        super().__init__()

        self.all_habits = Habit.load_all()
        self.child_windows = []

        #set the geometry and the title of the main window
        self.geometry("900x450")
        self.title("Habit Tracking App")

        self.top_frame = self.get_top_frame()
        self.top_frame.pack(side="top")

        self.center_frame = CenterFrame(self,column_names=self.HABIT_LIST_TITLES,
                                        habit_list=self.all_habits)
        self.center_frame.pack(side="top", fill="both")

        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.pack(side="bottom")

    def destroy(self):
        """
        Override the destroy method to ensure all child windows are closed
        before the main window is destroyed.

        Raises:
            AttributeError: Child window has no Attribute destroy.
        """
        try:
            for child in self.child_windows:
                #call the destroy methode in the child window
                child.destroy()
        except AttributeError as exc:
            raise AttributeError("Child window has no Attribute destroy.") from exc
        return super().destroy()

    def add_child_window(self, child):
        """
        Add a child window to the list and disable buttons in the bottom frame.
        
        Args:
            child (PopUpWindow): The child window to add.
        """
        self.child_windows.append(child)

        #disables button that there is only one child window at once.
        for button in self.bottom_frame.buttons:
            button.state(["disabled"])

    def remove_child_window(self,child):
        """
        Remove a child window from the list and enable buttons in the bottom frame.
        
        Args:
            child (PopUpWindow): The child window to remove.
        """
        self.child_windows.remove(child)
        for button in self.bottom_frame.buttons:
            button.state(["!disabled"])


    def get_top_frame(self):
        """
        Create and return the top frame of the application.
        
        Returns:
            ttk.Frame: The top frame containing the application title.
        """
        top_frame = ttk.Frame(self)
        #creates and pack title label
        title = ttk.Label(top_frame, text="Habit Tracking App")
        title.pack(side="top")
        #create and pack label with the value of the longest streak count.
        label = ttk.Label(top_frame,text="Overall longest streak is "\
                          f"{ana.get_longest_streak_of_all(habit_list=self.all_habits)}.")
        label.pack(side="top")
        return top_frame

    def reload_center_frame(self, habit_list):
        """
        Reload the center frame with updated habit data.
        
        Args:
            habit_list (list): The updated list of habits.
        """
        self.center_frame.destroy()
        self.center_frame = CenterFrame(self, App.HABIT_LIST_TITLES, habit_list)
        self.center_frame.pack(side="top", fill="both")


def main():
    """
    Name
        main
    
    DESCRIPTION
        Excecute the habit tracking app
    """
    app = App()
    app.mainloop()

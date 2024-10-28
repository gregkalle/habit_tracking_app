"""
NAME
    center_frame: Creat the center frame of the habit tracking app.

CLASSES
    ttk.Frame
        CenterFrame
"""
import tkinter as tk
from tkinter import ttk
from scr.analytics import Analytics

class CenterFrame(ttk.Frame):
    """
    The center frame of the habit tracking app.
    
    Attributes:
        COLUMN_OFFSET (int): The numbers of columns that are empty on the left of the grid.
        column_names (list): The list of the column names. Default is None.
        habit_list (list): The list of the habits shown in the center frame. Default is None.
        selected_habit_id (tkIntVar): The id of the selected radiobutton. Linked to the habit_id.
        buttons (list): The list of the shown radiobuttons.
    """
    COLUMN_OFFSET = 1

    def __init__(self, master, column_names=None, habit_list = None):
        super().__init__(master)

        self.column_names = column_names
        if self.column_names is None:
            self.column_names = []
        self.habit_list = habit_list
        if self.habit_list is None:
            self.habit_list = []
        self.selected_habit_id = tk.IntVar(self)
        self.buttons=[]

        self.set_column_names(self.column_names)
        self.pack_all_habits(self.habit_list)
        self.columnconfigure(0, minsize=10)


    def set_column_names(self, column_names):
        "Set the column names of the data table."
        try:
            for name in column_names:
                ttk.Label(self,text=name,anchor=tk.CENTER)\
                    .grid(column=column_names.index(name)+CenterFrame.COLUMN_OFFSET,
                    row=0,ipadx=10, ipady=20
                    )
        except TypeError as exc:
            raise TypeError("Column name is not iterable.") from exc

    def pack_all_habits(self, habit_list):
        """Packing the data of all habits in the data table of the center frame."""
        row = 1
        try:
            for habit in habit_list:
                try:
                    habit_data = Analytics.habit_to_dict(habit)
                except TypeError as exc:
                    raise TypeError("No object of type habit.") from exc
                self.pack_habit_data(habit_data, row)
                row += 1
        except TypeError as exc:
            raise TypeError("Habit list is not iterable.") from exc

    def pack_habit_data(self, habit_data, row):
        """Packing the data of one habit in the next empty row of the data table."""
        for name in habit_data.keys():
            if name == self.column_names[0]:
                ttk.Radiobutton(self,value=habit_data[name],variable=self.selected_habit_id)\
                    .grid(column=self.column_names.index(name)+CenterFrame.COLUMN_OFFSET,
                          row=row,ipadx=10)
            else:
                ttk.Label(self, text=habit_data[name],anchor=tk.CENTER)\
                    .grid(column=self.column_names.index(name)+CenterFrame.COLUMN_OFFSET,
                          row=row,ipadx=30,ipady=10)

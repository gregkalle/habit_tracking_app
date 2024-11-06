"""
NAME
    center_frame: Creat the center frame of the habit tracking app.

CLASSES
    ttk.Frame
        CenterFrame
"""
import tkinter as tk
from tkinter import ttk
from scr.habit import Habit

class CenterFrame(ttk.Frame):
    """
    The center frame of the habit tracking app.

    Args:
        master (tkinter.Tk): The main window of the habit tracking app.
        column_names (list): The Names of the columns of the table.
        habit_list (list): List of the habits witch will be shown in the table.
    
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
        self.selected_habit_id = []
        self.buttons=[]
        self.set_column_names(column_names=self.column_names)
        self.pack_all_habits(habit_list=self.habit_list)
        self.columnconfigure(0, minsize=10)

    def set_column_names(self, column_names):
        """
        Set the column names of the data table.
        
        Args:
            column_names (list): The name of the columns of the data table.

        Raises:
            TypeError: Object is not iterable.
        """
        try:
            for i,name in enumerate(column_names):
                ttk.Label(self,text=name,anchor=tk.CENTER)\
                    .grid(column=i+CenterFrame.COLUMN_OFFSET,
                    row=0,ipadx=10, ipady=20
                    )
        except TypeError as exc:
            raise TypeError("Object is not iterable.") from exc

    def pack_all_habits(self, habit_list):
        """
        Packing the data of all habits in the data table of the center frame.
        
        Args:
            habit_list (list): A list of the habit from which the data should be packed.

        Raises:
            TypeError: Object is not iterable.
            TypeError: Object not of type habit.
        """
        try:
            for row,habit in enumerate(habit_list,start=1):
                self.pack_habit(habit_data=Habit.habit_data(habit),row=row)
        except TypeError as exc:
            raise TypeError("Object is not iterable.") from exc

    def pack_habit(self, habit_data, row):
        """
        Packing the data of one habit in the next empty row of the data table.
        
        Args:
            habit_data (dict): The data of the habit that is added to the table.
            row (int): The row which the habit data is added to.

        Raises:
            TypeError: habit data no dictionary.
            TypeError: row is no integer.
        """
        #if not isinstance(habit_data,list):
        #    raise TypeError("habit is no Habit.")
        if not isinstance(row,int):
            raise TypeError("row is no integer.")
        for i,data in enumerate(habit_data):
            if i==0:
                variable = tk.IntVar()
                button = ttk.Checkbutton(self,onvalue=data,offvalue=None,
                                         variable=variable)
                self.selected_habit_id.append(variable)
                button.grid(column=i+CenterFrame.COLUMN_OFFSET,
                          row=row,ipadx=10)
            else:
                ttk.Label(self, text=str(data),anchor=tk.CENTER)\
                    .grid(column=i+CenterFrame.COLUMN_OFFSET,
                          row=row,ipadx=30,ipady=10)

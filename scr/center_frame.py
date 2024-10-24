from scr.analytics import Analytics
import tkinter as tk
from tkinter import ttk

class CenterFrame(ttk.Frame):
    
    COLUMN_OFFSET = 1
    
    def __init__(self, master, column_names, habit_list):
        super().__init__(master)

        self.column_names = column_names
        self.habit_list = habit_list
        self.selected_habit_id = tk.IntVar(self)
        self.buttons=[]

        self.set_column_names(self.column_names)
        self.pack_all_habits(self.habit_list)
        self.columnconfigure(0, minsize=10)


    def set_column_names(self, column_names):
        "set the columnames of the data table"
        for name in column_names:
            ttk.Label(self,text=name,anchor=tk.CENTER).grid(column=column_names.index(name)+CenterFrame.COLUMN_OFFSET, row=0,ipadx=10, ipady=20)
    
    def pack_all_habits(self, habit_list):
        """packing the data of all habits in the data table of the center frame"""
        row = 1
        for habit in habit_list:
            habit_data = Analytics.habit_to_dict(habit)
            self.pack_habit_data(habit_data, row)
            row += 1

    def pack_habit_data(self, habit_data, row):
        """packing the data of a habit in the data table of the center frame"""
        for name in habit_data.keys():
            if name == self.column_names[0]:
                ttk.Radiobutton(self,value=habit_data[name],variable=self.selected_habit_id).grid(column=self.column_names.index(name)+CenterFrame.COLUMN_OFFSET,row=row,ipadx=10)
            elif name == self.column_names[-1]:
                self.get_calendar(row=row)
            else:
                ttk.Label(self, text=habit_data[name],anchor=tk.CENTER).grid(column=self.column_names.index(name)+CenterFrame.COLUMN_OFFSET,row=row,ipadx=30,ipady=10)

    def get_calendar(self, row):
        column = len(self.column_names)-1 + CenterFrame.COLUMN_OFFSET
        button = ttk.Button(self,text="calendar",command=self.click_calendar,padding=10)
        button.grid(column=column,row=row)
        self.buttons.append(button)

    def click_calendar(self):
        pass



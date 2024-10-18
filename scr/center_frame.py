from scr.analytics import Analytics
import tkinter as tk
from tkinter import ttk

class CenterFrame(ttk.Frame):
    
    COLUMN_OFFSET = 1
    
    def __init__(self, master, column_names, habit_list):
        super().__init__(master)

        self.column_names = column_names
        self.habit_list = habit_list
        self.selected_habit_id = tk.IntVar()

        self.set_column_names(self.column_names)
        self.pack_all_habits(self.habit_list)
        self.columnconfigure(0, minsize=10)

        
        #self.children_frames = self.get_children_frames(self.column_names)
        #self.pack_all_habits(self.children_frames, self.habit_list)
        #self.pack_children_frames(self.children_frames)
       
        #self.pack_radio_buttons(self.get_radio_buttons(self.children_frames[self.column_names[0]], Analytics.get_habit_ids(self.habit_list)))

    def set_column_names(self, column_names):
        "set the columnames of the data table"
        for name in column_names:
            ttk.Label(self,text=name,anchor=tk.CENTER).grid(column=column_names.index(name)+CenterFrame.COLUMN_OFFSET, row=0,ipadx=10, ipady=20)
    
    def pack_all_habits(self, habit_list):
        """packing the data of all habits in the child frames of the center frame"""
        row = 1
        for habit in habit_list:
            habit_data = Analytics.habit_to_dict(habit)
            self.pack_habit_data(habit_data, row)
            row += 1

    def pack_habit_data(self, habit_data, row): 
        for name in habit_data.keys():
            if name == self.column_names[0]:
                ttk.Radiobutton(self,value=habit_data[name],variable=self.selected_habit_id).grid(column=self.column_names.index(name)+CenterFrame.COLUMN_OFFSET,row=row,ipadx=10)
            elif name == self.column_names[-1]:
                self.get_calender()
            else:
                ttk.Label(self, text=habit_data[name],anchor=tk.CENTER).grid(column=self.column_names.index(name)+CenterFrame.COLUMN_OFFSET,row=row,ipadx=30,ipady=10)


    def get_calender(self):
        pass    



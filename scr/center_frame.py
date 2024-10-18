from scr.analytics import Analytics
import tkinter as tk
from tkinter import ttk

class CenterFrame(ttk.Frame):
    
    def __init__(self, master, column_names, habit_list):
        super().__init__(master)

        self.column_names = column_names
        self.habit_list = habit_list
        self.selected_habit_id = tk.IntVar()

        self.set_column_names(self.column_names)
        
        #self.children_frames = self.get_children_frames(self.column_names)
        #self.pack_all_habits(self.children_frames, self.habit_list)
        #self.pack_children_frames(self.children_frames)
       
        #self.pack_radio_buttons(self.get_radio_buttons(self.children_frames[self.column_names[0]], Analytics.get_habit_ids(self.habit_list)))



    def get_children_frames(self, column_names):
        """get the frames for the data table"""
        children_frame = {}
        for name in column_names:
            frame = ttk.Frame(self, padding=10)
            children_frame[name] = frame
            ttk.Label(frame,text=name).grid(ipady=10)
        return children_frame
    
    def set_column_names(self, column_names):
        for name in column_names:
            ttk.Label(self,text=name).grid(column=column_names.index(name), row=0)
    
    def pack_children_frames(self, children_frames):
        """packing the children_frames to the center frame"""
        for child in children_frames.keys():
            children_frames[child].pack(side="left", fill="both")

    def pack_all_habits(self, children_frames, habit_list):
        """packing the data of all habits in the child frames of the center frame"""
        for habit in habit_list:
            habit_data = Analytics.habit_to_dict(habit)
            self.pack_habit_data(children_frames, habit_data)

    def pack_habit_data(self, children_frames, habit_data):
        for child in children_frames.keys():
            if child == self.column_names[0]:
                ttk.Radiobutton(children_frames[child],value=habit_data[child],variable=self.selected_habit_id).grid(ipady=10)
            elif child == self.column_names[-1]:
                self.get_calender()
            else:
                ttk.Label(children_frames[child], text=habit_data[child]).grid(ipady=10)


    def get_calender(self):
        pass    



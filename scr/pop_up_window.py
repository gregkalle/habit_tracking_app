from scr.analytics import Analytics
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb

class PopUpWindow(tk.Tk):

    BEHAVE_NEW_HABIT = "new habit"
    BEHAVE_CHANGE_HABIT = "change habit"

    
    def __init__(self, main_window, behave = BEHAVE_NEW_HABIT):
        super().__init__()
        
        self.behave = behave
        self.main_window = main_window
        self.main_window.add_child_window(self)

        self.habit_frequency = tk.IntVar(self)

        self.entry_habit_name = self.pack_name_entry_field(label_text="habit name")
        self.entry_habit_description = self.pack_name_entry_field(label_text="habit description")
        if self.behave == PopUpWindow.BEHAVE_NEW_HABIT:
            self.pack_frequency_entry_field(label_text="frequency",variable=self.habit_frequency)
        self.pack_buttons()
        
    def destroy(self):
        try:
            self.main_window.remove.child_window()
        except:
            pass
        return super().destroy()

    
    
    def pack_name_entry_field(self, label_text):
        """pack label and entry field and return the entry field"""
        frame = ttk.Frame(self)
        ttk.Label(frame,anchor="w", text=label_text,padding=10).pack(side="left")
        textbox = ttk.Entry(frame)
        textbox.pack(side="left")
        frame.pack()
        return textbox

    def pack_frequency_entry_field(self, label_text, variable):
        frame = ttk.Frame(self)
        ttk.Label(frame,anchor="w", text=label_text,padding=10).pack(side="left")
        for text in self.main_window.USABLE_FREQUENCIES:
            ttk.Radiobutton(frame,text=text.lower(),value=self.main_window.USABLE_FREQUENCIES[text],
                            variable=variable).pack(side="left")
        frame.pack()
    
    def pack_buttons(self):
        button_frame = ttk.Frame(self)
        ttk.Button(button_frame, text="OK", command=self.click_ok, padding=10).pack(side="left")
        ttk.Button(button_frame, text="Cancle", command=self.destroy, padding=10).pack(side="left")
        button_frame.pack(side="bottom")

    
    def click_ok(self):
        if self.behave == PopUpWindow.BEHAVE_NEW_HABIT:
            self.click_okay_new_habit()
        if self.behave == PopUpWindow.BEHAVE_CHANGE_HABIT:
            self.click_okay_change_habit()


    def click_okay_new_habit(self):
        if not (self.entry_habit_name.get() and self.entry_habit_description.get() and self.habit_frequency.get()):
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="The name and description of your habit may not be empty and you must select a frequency"
                       )
            message.show()
        else:
            habit = Analytics.create_new_habit(habit_name=self.entry_habit_name.get(),
                                       habit_description=self.entry_habit_description.get(),
                                       frequency=self.habit_frequency.get())
            try:
                self.main_window.analytics.all_habits.append(habit)
            except AttributeError:
                pass
            except:
                pass
            
            try:
                self.main_window.reload_center_frame(self.main_window.analytics.all_habits)
            except AttributeError:
                pass
            except:
                pass
            
            self.destroy()

    def click_okay_change_habit(self):
        if not self.main_window.center_frame.selected_habit_id.get():
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="No habit selected"
                       )
            message.show()
            self.destroy()     
        elif not (self.entry_habit_name.get() or self.entry_habit_description.get()):
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="The name and description of your habit may not be empty",
                       )
            message.show()
        else:
                if self.entry_habit_name.get():
                    Analytics.change_habit_name(habit_id=self.main_window.center_frame.selected_habit_id.get(),
                                                habit_name=self.entry_habit_name.get())
                    self.main_window.analytics.load_habits()
                    self.main_window.reload_center_frame(self.main_window.analytics.all_habits)

                if self.entry_habit_description.get():
                    Analytics.change_habit_description(habit_id=self.main_window.center_frame.selected_habit_id.get(),
                                                habit_description=self.entry_habit_description.get())
                    self.main_window.analytics.load_habits()
                    self.main_window.reload_center_frame(self.main_window.analytics.all_habits)
                self.destroy()
        

 
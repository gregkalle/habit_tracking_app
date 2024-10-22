from scr.analytics import Analytics
import tkinter as tk
from tkinter import ttk
from scr.pop_up_window import PopUpWindow
import tkinter.messagebox as mb

class EntryPopUp(PopUpWindow):

    """
    A pop-up window for entering or changing habit details.
    
    Attributes:
        BEHAVE_NEW_HABIT (str): Constant for "new habit" behavior.
        BEHAVE_CHANGE_HABIT (str): Constant for "change habit" behavior.
    """

    BEHAVE_NEW_HABIT = "new habit"
    BEHAVE_CHANGE_HABIT = "change habit"

    
    def __init__(self, main_window, behave = BEHAVE_NEW_HABIT):
        """
        Initialize the entry pop-up window.
        
        Args:
            main_window (Tk): The main application window.
            behave (str): The behavior mode of the pop-up (new habit or change habit).
        """
        super().__init__(main_window=main_window)
        
        self.behave = behave
        self.title(self.behave)

        self.habit_frequency = tk.IntVar(self)

        self.entry_habit_name = self.pack_name_entry_field(label_text="habit name")
        self.entry_habit_description = self.pack_name_entry_field(label_text="habit description")
        if self.behave == EntryPopUp.BEHAVE_NEW_HABIT:
            self.pack_frequency_entry_field(label_text="frequency",variable=self.habit_frequency)
        self.pack_buttons()
        
    
    def pack_name_entry_field(self, label_text):
        """
        Pack label and entry field and return the entry field.
        
        Args:
            label_text (str): The text for the label.
        
        Returns:
            ttk.Entry: The entry field widget.
        """
        frame = ttk.Frame(self)
        ttk.Label(frame,anchor="w", text=label_text,padding=10).pack(side="left")
        textbox = ttk.Entry(frame)
        textbox.pack(side="left")
        frame.pack()
        return textbox

    def pack_frequency_entry_field(self, label_text, variable):
        """
        Pack label and radio buttons for frequency selection.
        
        Args:
            label_text (str): The text for the label.
            variable (tk.IntVar): The variable to store the selected frequency.
        """
        frame = ttk.Frame(self)
        ttk.Label(frame,anchor="w", text=label_text,padding=10).pack(side="left")
        for text in self.main_window.USABLE_FREQUENCIES:
            ttk.Radiobutton(frame,text=text.lower(),value=self.main_window.USABLE_FREQUENCIES[text],
                            variable=variable).pack(side="left")
        frame.pack()
    
    def pack_buttons(self):
        """
        Create and pack the buttons for the entry pop-up window.
        """
        button_frame = ttk.Frame(self)
        ttk.Button(button_frame, text="OK", command=self.click_ok, padding=10).pack(side="left")
        ttk.Button(button_frame, text="Cancel", command=self.destroy, padding=10).pack(side="left")
        button_frame.pack(side="bottom")

    
    def click_ok(self):
        """
        Handle the OK button click based on the behavior mode.
        """
        if self.behave == EntryPopUp.BEHAVE_NEW_HABIT:
            self.click_okay_new_habit()
        if self.behave == EntryPopUp.BEHAVE_CHANGE_HABIT:
            self.click_okay_change_habit()


    def click_okay_new_habit(self):
        """
        Handle the creation of a new habit.
        """
        if not (self.entry_habit_name.get() and self.entry_habit_description.get() and self.habit_frequency.get()):
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="The name and description of your habit may not be empty and you must select a frequency"
                       )
            message.show()
        else:
            habit = Analytics.create_new_habit(habit_name=self.entry_habit_name.get(),
                                       habit_description=self.entry_habit_description.get(),
                                       frequency=self.habit_frequency.get())
            habit.save()
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
        """
        Handle the modification of an existing habit.
        """  
        if not (self.entry_habit_name.get() or self.entry_habit_description.get()):
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="The name and description of your habit may not be empty",
                       )
            message.show()
        else:
                habit = Analytics.change_habit_name_description(habit_id=self.main_window.center_frame.selected_habit_id.get(),
                                                        habit_name=self.entry_habit_name.get(),
                                                        habit_description=self.entry_habit_description.get())
                habit.save()
                self.main_window.analytics.load_habits()
                self.main_window.reload_center_frame(self.main_window.analytics.all_habits)
        self.destroy()
        

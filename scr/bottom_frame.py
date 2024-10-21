from scr.analytics import Analytics
from scr.pop_up_window import DatePicker
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from scr.entry_window import EntryPopUp



class BottomFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.BUTTONS = {"check date" : self.click_check_date,
                        "new habit" : self.click_new_habit,
                        "change habit" : self.click_change_habit,
                        "delete habit" : self.click_delete_habit
                        }

        self.selected_frequency = tk.StringVar()
        self.selected_value = tk.StringVar()

        for button in self.BUTTONS.keys():
            self.get_button(frame=self,text=button,function=self.BUTTONS[button]).pack(side="left")
        
        self.get_menu_button(frame=self,title="select periodicity",item_selection=master.SELECTABLE_FREQUENCIES,
                             selected_item=self.selected_frequency).pack(side="left")
        self.get_menu_button(frame=self,title="sort by value",item_selection=master.SELECTABLE_VALUES
                             ,selected_item=self.selected_value).pack(side="left")
        
        self.selected_frequency.trace_add("write",self.frequency_selected)
        self.selected_value.trace_add("write",self.value_selected)

    def get_menu_button(self, frame, title, item_selection, selected_item):
        """
        get a menu button 
        """

        menu_button = ttk.Menubutton(frame, text=title)
        menu = tk.Menu(menu_button)

        for item in item_selection:
            menu.add_radiobutton(
                label=item,
                value=item.upper(),
                variable=selected_item
            )
        menu_button["menu"] = menu
        return menu_button
    
    def get_button(self, frame, text, function):
        """get a button"""
        return ttk.Button(frame, text=text, command=function, padding=10)
    
    def click_check_date(self):
        if not self.master.center_frame.selected_habit_id.get():
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="No habit selected"
                       )
            message.show()
        else:
            calender = DatePicker(self.master)

    def click_new_habit(self):
        pop_up_window = EntryPopUp(master=self.master)

    def click_change_habit(self):
        if not self.master.center_frame.selected_habit_id.get():
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                                message="No habit selected"
                               )
            message.show()
        else:
            pop_up_window = EntryPopUp(master=self.master, behave=EntryPopUp.BEHAVE_CHANGE_HABIT)

    def click_delete_habit(self):
        """delet the selected habit"""
        if not self.master.center_frame.selected_habit_id.get():
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="No habit selected"
                       )
            message.show()
        else:    
            message = mb.askokcancel(title="Delete",
                                     message=f"Do you want to delete the selected habit with the id {self.master.center_frame.selected_habit_id.get()}?"                                     
                                     )
            if message:
                Analytics.delete_habit(habit_id=self.master.center_frame.selected_habit_id.get())
                self.master.analytics.load_habits()
                self.master.reload_center_frame(self.master.analytics.all_habits)

    def frequency_selected(self, *args):
        """Execute the reload_center_frame methode in the master frame with the habits of the right frequency"""
        frequency_name = self.selected_frequency.get()
        if frequency_name in self.master.USABLE_FREQUENCIES.keys():
            habit_list = Analytics.get_habits_with_frequency(self.master.analytics.all_habits, self.master.USABLE_FREQUENCIES[frequency_name])
        else:
            habit_list = self.master.analytics.all_habits

        self.master.reload_center_frame(habit_list)
            
    def value_selected(self, *args):
        self.master.reload_center_frame(Analytics.HABIT_LIST_TITLES, self.master.analytics.all_habits)

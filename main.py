from scr.analytics import Analytics
from scr.center_frame import CenterFrame
import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    """
    """
    USABLE_FREQUENCIES = {"WEEKLY" : 7, "DAILY" : 1}
    SELECTABLE_VALUES = ("frequency", "current streak", "longest streak")
    SELECTABLE_FREQUENCIES = ("Daily", "Weekly", "All")

    def __init__(self):
        super().__init__()

        self.analytics = Analytics()

        self.BUTTONS = {"check date" : self.click_check_date,
                        "new habit" : self.click_new_habit,
                        "change habit" : self.click_change_habit,
                        "delete habit" : self.click_delete_habit
                        }

        self.geometry("800x400")
        self.title("Habit Tracking App")

        self.selected_habit_id = tk.IntVar()
        self.selected_frequency = tk.StringVar()
        self.selected_value = tk.StringVar()

        self.top_frame = self.get_top_frame().pack(side="top")
        self.get_bottom_frame().pack(side="bottom")
        self.center_frame = CenterFrame(self, Analytics.HABIT_LIST_TITLES, self.analytics.all_habits)
        self.center_frame.pack(side="top", fill="both")

        self.selected_frequency.trace_add("write",self.frequency_selected)
        self.selected_value.trace_add("write",self.value_selected)

      

    def get_top_frame(self):
        top_frame = ttk.Frame(self)
        title = ttk.Label(top_frame, text="Habit Tracking App")
        title.pack()
        return top_frame 
       

    def get_bottom_frame(self):
        bottom_frame = ttk.Frame(self)
        
        
        for button in self.BUTTONS.keys():
            self.get_button(bottom_frame,button,self.BUTTONS[button]).pack(side="left")
        
        self.get_menu_button(bottom_frame,"select periodicity",App.SELECTABLE_FREQUENCIES,
                             self.selected_frequency).pack(side="left")
        self.get_menu_button(bottom_frame,"sort by value",App.SELECTABLE_VALUES,self.selected_value).pack(side="left")
        
        return bottom_frame

    def get_menu_button(self, frame, title, item_selection, selected_item):

        menu_button = ttk.Menubutton(frame, text=title)
        menu = tk.Menu(menu_button)

        for select in item_selection:
            menu.add_radiobutton(
                label=select,
                value=select.upper(),
                variable=selected_item
            )
        menu_button["menu"] = menu
        return menu_button


    def get_button(self, frame, text, function):
        return ttk.Button(frame, text=text, command=function, padding=10)
    
    def get_radio_buttons(self, frame, integer_list):
        return [ttk.Radiobutton(frame, value=integer, variable=self.selected_habit_id) for integer in integer_list]
    
    def frequency_selected(self, *args):
        frequency_name = self.selected_frequency.get()
        if frequency_name in App.USABLE_FREQUENCIES.keys():
            habit_list = Analytics.get_habits_with_frequency(self.analytics.all_habits, App.USABLE_FREQUENCIES[frequency_name])
        else:
            habit_list = self.analytics.all_habits

        self.reload_center_frame(Analytics.HABIT_LIST_TITLES,habit_list)
            

    def value_selected(self, *args):
        self.reload_center_frame(Analytics.HABIT_LIST_TITLES, self.analytics.all_habits)

    def click_check_date(self):
        pass

    def click_new_habit(self):
        pass

    def click_change_habit(self):
        pass

    def click_delete_habit(self):
        pass

    def reload_center_frame(self, column_names, habit_list):
        self.center_frame.destroy()
        self.center_frame = CenterFrame(self, column_names, habit_list)
        self.center_frame.pack(side="top", fill="both")


if __name__ == "__main__":
    app = App()
    app.mainloop()
from scr.analytics import Analytics
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

        self.create_top_frame()
        self.create_bottom_frame()



        self.selected_frequency.trace_add("write",self.frequency_selected)
        self.selected_value.trace_add("write",self.value_selected)


    def create_top_frame(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(side="top")

        title = ttk.Label(top_frame, text="Habit Tracking App")
        title.pack()
    """
    def create_center_frame(self):
        center_frame = ttk.Frame(self)
        center_frame.pack(side="top", fill="both")

        frames_in_center ={}
        for name in self.HABIT_LIST_TITLES:
            frames_in_center[name] = ttk.Frame(master=center_frame, padding=10)
            frames_in_center[name].pack(side="left", fill="both")
        
            label = ttk.Label(frames_in_center[name], text=name)
            label.pack(side="top", fill="both")

        for get_radio_buttons(frames_in_center[HABIT_LIST_TITLES[0]],[1,2,3,4,5])

    def load_habits(self, habit_list):
        for habit in habit_list:
            frames_in_center[name] = ttk.Frame(master=center_frame, padding=10)
            frames_in_center[name].pack(side="left", fill="both")
        
            label = ttk.Label(frames_in_center[name], text=name)
            label.pack(side="top", fill="both")
    """


    def create_bottom_frame(self):
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(side="bottom")
        
        for button in self.BUTTONS.keys():
            self.get_button(bottom_frame,button,self.BUTTONS[button]).pack(side="left")
        
        self.get_menu_button(bottom_frame,"select periodicity",App.SELECTABLE_FREQUENCIES,
                             self.selected_frequency).pack(side="left")
        self.get_menu_button(bottom_frame,"sort by value",App.SELECTABLE_VALUES,self.selected_value).pack(side="left")


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
        print(self.selected_frequency.get())

    def value_selected(self, *args):
        print(self.selected_value.get())

    def click_check_date(self):
        pass

    def click_new_habit(self):
        pass

    def click_change_habit(self):
        pass

    def click_delete_habit(self):
        pass



if __name__ == "__main__":
    app = App()
    app.mainloop()
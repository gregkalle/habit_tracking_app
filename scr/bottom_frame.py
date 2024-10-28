"""
NAME
    bottom_frame: Create the bottom frame of the habit tracking app.

CLASSES
    ttk.Frame
        BottomFrame        
"""
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from scr.analytics import Analytics
from scr.entry_window import EntryPopUp, DatePicker, PopUpCalendar


class BottomFrame(ttk.Frame):
    """
    The bottom frame of the habit tracking app.
    
    Attributes:
        selected_frequency (tkinter.StringVar): The selected frequency of the menubutton
        buttons (list): The buttons shown in the bottom frame.
    """
    def __init__(self, master):
        super().__init__(master)

        self.__buttons_def = {"check date" : self.click_check_date,
                        "new habit" : self.click_new_habit,
                        "change habit" : self.click_change_habit,
                        "delete habit" : self.click_delete_habit,
                        "calendar" : self.click_calendar
                        }

        self.selected_frequency = tk.StringVar()

        self.buttons = []
        for button_name, button_function in self.__buttons_def.items():
            button = ttk.Button(master=self,text=button_name,command=button_function,padding=10)
            button.pack(side="left")
            self.buttons.append(button)

        try:
            self.get_menu_button(frame=self,title="select periodicity",
                                item_selection=master.SELECTABLE_FREQUENCIES,
                                selected_item=self.selected_frequency).pack(side="left")
        except AttributeError as exc:
            raise AttributeError("No selectable frequencies attribute in master object.") from exc


        self.selected_frequency.trace_add("write",self.frequency_selected)


    def get_menu_button(self, frame, title, item_selection, selected_item):
        """
        Get a menu button

        Args:
            frame (ttk.frame): The parent frame of the menu button.
            title (str): The title of the button.
            item_selection (tuple): The items of the menubutton.
            selected_item (tk.StringVar): The variable witch saves the selected item of the menu button.

        Returns:
            ttk.Menubutton the menu button widget.
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

    def click_check_date(self):
        if not self.master.center_frame.selected_habit_id.get():
            self.show_no_habit_selected()
        else:
            DatePicker(main_window=self.master)

    def click_new_habit(self):
        EntryPopUp(main_window=self.master)

    def click_change_habit(self):
        if not self.master.center_frame.selected_habit_id.get():
            self.show_no_habit_selected()
        else:
            EntryPopUp(main_window=self.master, behave=EntryPopUp.BEHAVE_CHANGE_HABIT)

    def click_delete_habit(self):
        """delet the selected habit"""
        try:
            habit_id = self.master.center_frame.selected_habit_id.get()
        except AttributeError as exc:
            raise AttributeError("No attribute get in master") from exc
        if not habit_id:
            self.show_no_habit_selected()
        else:
            message = mb.askokcancel(title="Delete",
                                    message=f"Do you want to delete the selected habit with the id\
                                    {self.master.center_frame.selected_habit_id.get()}?"
                                    )
            if message:
                Analytics.delete_habit(habit_id=habit_id)
                try:
                    self.master.analytics.all_habits = Analytics.load_habits()
                    self.master.reload_center_frame(self.master.analytics.all_habits)
                except AttributeError as exc:
                    raise AttributeError("No attribute analytics in master.") from exc
    def click_calendar(self):
        if not self.master.center_frame.selected_habit_id.get():
            self.show_no_habit_selected()
        else:
            try:
                habit_id = self.master.center_frame.selected_habit_id.get()
            except AttributeError as exc:
                raise AttributeError("There are no attribute center frame in the master") from exc

            habit = Analytics.get_current_tracked_habit(habit_id=habit_id)
            if habit is None:
                raise ValueError("There are no habit insert to show calendar")

            completed_dates = habit.completion.completed_dates
            frequency = habit.completion.frequency
            PopUpCalendar(main_window=self.master,completed_dates=completed_dates,
                          frequency=frequency)


    def frequency_selected(self,*args):
        """Execute the reload_center_frame methode in the master\
            frame with the habits of the right frequency"""
        frequency_name = self.selected_frequency.get()
        if frequency_name in self.master.USABLE_FREQUENCIES.keys():
            habit_list = Analytics.get_habits_with_frequency(
                self.master.analytics.all_habits, self.master.USABLE_FREQUENCIES[frequency_name])
        else:
            habit_list = self.master.analytics.all_habits
        self.master.reload_center_frame(habit_list)
        #return args to prevent unused argument Pylint warning
        return args

    def show_no_habit_selected(self):
        message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                            message="No habit selected"
                            )
        message.show()

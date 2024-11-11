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
import scr.analytics as ana
from scr.habit import Habit
from scr.entry_window import EntryPopUp, DatePicker, PopUpCalendar


class BottomFrame(ttk.Frame):
    """
    The bottom frame of the habit tracking app.

    Args:
        master (tkinter.Tk): Main window of the habit tracking app
    
    Attributes:
        selected_frequency (tkinter.StringVar): The selected frequency of the menubutton
        buttons (list): The buttons shown in the bottom frame.

    Raises:
        AttributeError: No selectable frequencies attribute in master.
    """
    def __init__(self, master):
        super().__init__(master)

        #define the name and function of the buttons in the buttom_frame
        self.__buttons_def = {"check date" : self.click_check_date,
                        "new habit" : self.click_new_habit,
                        "change habit" : self.click_change_habit,
                        "delete habit" : self.click_delete_habit,
                        "calendar" : self.click_calendar
                        }

        self.selected_frequency = tk.StringVar()

        self.buttons = []
        #create and pack buttons
        for button_name, button_function in self.__buttons_def.items():
            button = ttk.Button(master=self,text=button_name,command=button_function,padding=10)
            button.pack(side="left")
            #save buttons in list that buttons can be seted disabled and enabled
            self.buttons.append(button)

        try:
            #create and set the menubutton to select frequencies and selected habits.
            self.get_menu_button(frame=self,title="show habits",
                                item_selection=self.master.SELECTABLE_FREQUENCIES,
                                selected_item=self.selected_frequency).pack(side="left")
        except AttributeError as exc:
            raise AttributeError("No selectable frequencies attribute in master.") from exc

        #trace the selected frequency to call frequency selected
        self.selected_frequency.trace_add("write",self.frequency_selected)


    def get_menu_button(self, frame, title, item_selection, selected_item):
        """
        Get a menu button

        Args:
            frame (ttk.frame): The parent frame of the menu button.
            title (str): The title of the button.
            item_selection (tuple): The items of the menubutton.
            selected_item (tk.StringVar): The variable which saves the selected
                                          item of the menu button.

        Returns:
            ttk.Menubutton the menu button widget.

        Raises:
            TypeError: Item selection is not iterable.
            
        """
        #create the menubutton
        menu_button = ttk.Menubutton(frame, text=title)
        menu = tk.Menu(menu_button)
        try:
            #create the radiobuttons of the menubutton
            for item in item_selection:
                menu.add_radiobutton(
                    label=item,
                    value=item,
                    variable=selected_item
                )
        except TypeError as exc:
            raise TypeError("Item selection is not iterable.") from exc
        menu_button["menu"] = menu
        return menu_button

    def click_check_date(self):
        """
        Takes action when the check dates button is clicked.

        If no habit is or more then one habit are selected, it shows an input error message.
        Else it creates a new date picker window.

        Raises:
            AttributeError: Selected habit id does not exist or has no Attribute get().
        """
        try:
            #saves the values of the selected_habit_id to a list.
            #x.get() is False if x not selected.
            values = list(map(lambda x: x.get(), self.master.center_frame.selected_habit_id))
        except AttributeError as exc:
            raise AttributeError("""Selected habit id does not exist
                                 or has no Attribute get().""") from exc
        #shortens values only to the selected values.
        values = [v for v in values if v]

        #shows datepicker only if one habit is selected
        if len(values) == 1:
            try:
                DatePicker(main_window=self.master, habit_id=values[0])
            except AttributeError as exc:
                raise AttributeError("""Selected habit id does not exist
                                        or has no Attribute get().""") from exc
        else:
            #shows input error message
            self.show_no_habit_selected()


    def click_new_habit(self):
        """
        Takes action when the new habit button is clicked.

        It creates a new entry window to insert a new habit.
        """
        EntryPopUp(main_window=self.master,habit_id=None)

    def click_change_habit(self):
        """
        Takes action when the change habit button is clicked.

        If no habit is or more then one habit are selected, it shows an input error message.
        Else it creates a new entry window to change the name
        or the description of an existing habit.

        Raises:
            AttributeError: Selected habit id does not exist or has no Attribute get().
        """
        try:
            #saves the values of the selected_habit_id to a list.
            #x.get() is False if x not selected.
            values = list(map(lambda x: x.get(), self.master.center_frame.selected_habit_id))
        except AttributeError as exc:
            raise AttributeError("""Selected habit id does not exist
                                 or has no Attribute get().""") from exc
        #shortens values only to the selected values.
        values = [v for v in values if v]
        #shows entry window only if one habit is selected
        if len(values) == 1:
            try:
                EntryPopUp(main_window=self.master,habit_id=values[0],
                           behave=EntryPopUp.BEHAVE_CHANGE_HABIT)
            except AttributeError as exc:
                raise AttributeError("""Selected habit id does not exist
                                    or has no Attribute get().""") from exc
        else:
            #shows input error message
            self.show_no_habit_selected()

    def click_delete_habit(self):
        """
        Takes action when the delete habit button is clicked.

        If no habit is or more then one habit are selected, it shows an input error message.
        Else it shows a ask-ok-cancel message. If this message returns okay,
        the selected habit is deleted from the database and the center frame
        will be reloaded.

        Raises:
            AttributeError: Selected habit id does not exist or has no Attribute get().
            AttributeError: No attribute analytics in master.
            AttributeError: No attribute reload center frame in master.
        """

        try:
            #saves the values of the selected_habit_id to a list.
            #x.get() is False if x not selected.
            values = list(map(lambda x: x.get(), self.master.center_frame.selected_habit_id))
        except AttributeError as exc:
            raise AttributeError("""Selected habit id does not exist
                                 or has no Attribute get().""") from exc

        #shortens values only to the selected values.
        values = [v for v in values if v]
        #shows ok/cancle message only if one habit is selected
        if len(values) == 1:
            message = mb.askokcancel(title="Delete",
                                    message=f"Do you want to delete the selected habit with the id\
                                    {values[0]}?"
                                    )
            if message:
                #if ok, the habit will be deleted
                Habit.delete(habit_id=values[0])
                try:
                    #reload all habits
                    self.master.all_habits = Habit.load_all()
                except AttributeError as exc:
                    raise AttributeError("No attribute analytics in master.") from exc
                try:
                    #reload the center frame
                    self.master.reload_center_frame(self.master.all_habits)
                except AttributeError as exc:
                    raise AttributeError("No attribute reload center frame in master.") from exc
        else:
            #shows input error message
            self.show_no_habit_selected()

    def click_calendar(self):
        """
        Takes action when the calendar button is clicked.

        If no habit is or more then one habit are selected, it shows an input error message.
        Else it create a new pop-up-calendar to show the dates when the habit is completed.

        Raises:
            AttributeError: Selected habit id does not exist or has no Attribute get().
            ValueError: There is no Habit object insert to show calendar.
        """
        try:
            #saves the values of the selected_habit_id to a list.
            #x.get() is False if x not selected.
            values = list(map(lambda x: x.get(), self.master.center_frame.selected_habit_id))
        except AttributeError as exc:
            raise AttributeError("""Selected habit id does not exist
                                 or has no Attribute get().""") from exc

        #shortens values only to the selected values.
        values = [v for v in values if v]
        #shows ok/cancle message only if one habit is selected
        if len(values) == 1:
            try:
                habit_id = values[0]
                habit = ana.get_current_tracked_habit(habit_list=self.master.all_habits,
                                                      habit_id=habit_id)
                if habit is None:
                    raise ValueError("There is no habit insert to show calendar.")

                completed_dates = habit["completed_dates"]
                frequency = habit["frequency"]
                creation_date = habit["creation_time"].date()
                #creates a calendar pop up window
                PopUpCalendar(main_window=self.master,completed_dates=completed_dates,
                            frequency=frequency, creation_date=creation_date)
            except AttributeError as exc:
                raise AttributeError("""Selected habit id does not exist
                                    or has no Attribute get().""") from exc
        else:
            #shows input error message
            self.show_no_habit_selected()

    def frequency_selected(self,*args):
        """
        Takes action when a frequency is selected.

        Execute the reload_center_frame methode in the master
        frame with the habits of the right frequency or selected habits

        Raises:
            AttributeError: The is no attribute USABLE_FREQUENCIES in master.
            AttributeError: The is no attribute analytics in master.
            AttributeError: The is no attribute reload center frame in master.
        """
        frequency_name = self.selected_frequency.get()
        try:
            #check frequency
            if frequency_name in self.master.USABLE_FREQUENCIES.keys():
                try:
                    #get the habits with selected frequency
                    habit_list = ana.get_habit_with_frequency(
                        self.master.all_habits,
                        self.master.USABLE_FREQUENCIES[frequency_name])
                except AttributeError() as exc:
                    raise AttributeError("The is no attribute analytics in master.") from exc
            #SELECTABLE_FREQUENCIES[2] = "Selected"
            elif frequency_name == self.master.SELECTABLE_FREQUENCIES[2]:
                #get all selected frequencies
                try:
                    #saves the values of the selected_habit_id to a list.
                    #x.get() is False if x not selected.
                    values = list(map(lambda x: x.get(),
                                      self.master.center_frame.selected_habit_id))
                except AttributeError as exc:
                    raise AttributeError("""Selected habit id does not exist
                                        or has not Attribute get().""") from exc
                #shortens values only to the selected values.
                values = [v for v in values if v]
                try:
                    #get all current tracked habits in habit_list
                    habit_list = ana.get_all_current_tracked_habits(\
                        habit_list=self.master.all_habits,id_list=values)
                except AttributeError() as exc:
                    raise AttributeError("The is no attribute analytics in master.") from exc
            else:
                try:
                    #get all habits
                    habit_list = self.master.all_habits
                except AttributeError() as exc:
                    raise AttributeError("Tere is no attribute analytics in master.")from exc
            try:
                #Reload the center frame to show selected habits in app
                self.master.reload_center_frame(habit_list)
            except AttributeError() as exc:
                raise AttributeError("The is no attribute reload center frame in master") from exc
        except AttributeError() as exc:
            raise AttributeError("There is no attribute USABLE_FREQUENCIES in master.") from exc
        #return args to prevent unused argument Pylint warning
        return args

    def show_no_habit_selected(self):
        """
        The error message which will be shown when no habit is or more than one habit are selected.
        """
        message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                            message="No or more than one habit selected."
                            )
        message.show()

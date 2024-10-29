"""
NAME
    entry_window - create a pop-up window of the habit tracking app

CLASSES
    pop_up_wondow.PopUpWindow
        EntryPopUp
        DatePicker
        PopUpCalendar
"""
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from datetime import date, timedelta
from tkcalendar import Calendar
from scr.pop_up_window import PopUpWindow
from scr.analytics import Analytics

class EntryPopUp(PopUpWindow):

    """
    A pop-up window for entering or changing habit details.

    Args:
        main_window (tkinter.Tk): The main application window.
        behave (str): Behaviour of the entry window. Insert EntryPopUp.BEHAVE_NEW_HABIT
            for new habit pop-up window or EntryPopUp.BEHAVE_CHANGE_HABIT for change habit window.
            Default is EntryPopUp.BEHAVE_NEW_HABIT.
    
    Attributes:
        BEHAVE_NEW_HABIT (str): Constant for new habit behaviour.
        BEHAVE_CHANGE_HABIT (str): Constant for change habit behaviour.
    """

    BEHAVE_NEW_HABIT = "new habit"
    BEHAVE_CHANGE_HABIT = "change habit"


    def __init__(self, main_window, behave = BEHAVE_NEW_HABIT):
        """
        Initialize the entry pop-up window.
        
        Args:
            main_window (Tk): The main application window.
            behave (str): The behavior mode of the pop-up (new habit or change habit).

        Raises:
            ValueError: Behave must be BEHAVE_NEW_HABIT or BEHAVE_CHANGE_HABIT

        """
        super().__init__(main_window=main_window)

        self.behave = behave
        if (self.behave == EntryPopUp.BEHAVE_NEW_HABIT and
               self.behave ==EntryPopUp.BEHAVE_CHANGE_HABIT):
            raise ValueError("Behave must be BEHAVE_NEW_HABIT or BEHAVE_CHANGE_HABIT")
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
        ttk.Label(frame,anchor="w",text=label_text,padding=10).pack(side="left")
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

        Raises:
            AttributeError: Main window has no attribut USABLE_FREQUENCIES
        """
        frame = ttk.Frame(self)
        ttk.Label(frame,anchor="w",text=label_text,padding=10).pack(side="left")
        try:
            for text in self.main_window.USABLE_FREQUENCIES:
                ttk.Radiobutton(frame,text=text.lower(),
                                value=self.main_window.USABLE_FREQUENCIES[text],
                                variable=variable).pack(side="left")
        except AttributeError as exc:
            self.destroy()
            raise AttributeError("Main window has no attribut USABLE_FREQUENCIES") from exc
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
        elif self.behave == EntryPopUp.BEHAVE_CHANGE_HABIT:
            self.click_okay_change_habit()


    def click_okay_new_habit(self):
        """
        Handle the creation of a new habit.

        Raises:
            AttributeError: Main window has no attribute all_habits
            AttributeError: Main window has no attribute reload center frame
        """
        if not (self.entry_habit_name.get() and self.entry_habit_description.get()\
                and self.habit_frequency.get()):
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="""The name and description of your habit may not be
                        empty and you must select a frequency"""
                       )
            message.show()
        else:
            habit = Analytics.create_new_habit(habit_name=self.entry_habit_name.get(),
                                       habit_description=self.entry_habit_description.get(),
                                       frequency=self.habit_frequency.get())
            habit.save()
            try:
                self.main_window.analytics.all_habits.append(habit)
            except AttributeError as exc:
                self.destroy()
                raise AttributeError("Main window has no attribute all_habits"
                                     ) from exc


            try:
                self.main_window.reload_center_frame(self.main_window.analytics.all_habits)
            except AttributeError as exc:
                self.destroy()
                raise AttributeError("Main window has no attribute reload center frame"
                                     ) from exc
            self.destroy()

    def click_okay_change_habit(self):
        """
        Handle the modification of an existing habit.

        Raises:
            AttributeError: Main window has no attribute center frame or selected habid id.
            AttributeError: Main window has no attribute load habits or all habits.
        """
        if not (self.entry_habit_name.get() or self.entry_habit_description.get()):
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="The name and description of your habit may not be empty",
                       )
            message.show()
        else:
            try:
                habit = Analytics.change_habit_name_description\
                    (habit_id=self.main_window.center_frame.selected_habit_id.get(),
                    habit_name=self.entry_habit_name.get(),
                    habit_description=self.entry_habit_description.get())
            except AttributeError as exc:
                self.destroy()
                raise AttributeError("""Main window has no attribute center frame
                                     or selected habid id.""") from exc
            habit.save()
            try:
                self.main_window.analytics.all_habits=Analytics.load_habits()
                self.main_window.reload_center_frame(self.main_window.analytics.all_habits)
            except AttributeError as exc:
                self.destroy()
                raise AttributeError("""Main window has no attribute load habits or
                                    all habits.""") from exc
        self.destroy()


class DatePicker(PopUpWindow):

    """
    A pop-up window for selecting dates using a calendar widget.
    """

    def __init__(self, main_window):
        """
        Initialize the date picker window.
        
        Args:
            main_window (Tk): The main application window.
        """
        super().__init__(main_window=main_window)

        self.title("select date")
        self.calendar = Calendar(master=self, selectmode="day")
        self.calendar.pack()
        self.pack_buttons()

    def pack_buttons(self):
        """
        Create and pack the buttons for the date picker window.
        """
        button_frame = ttk.Frame(self)
        ttk.Button(button_frame, text="today", command=self.click_today,
               padding=10).pack(side="left")
        ttk.Button(button_frame, text="select date", command=self.click_date,
               padding=10).pack(side="left")
        ttk.Button(button_frame, text="Cancel", command=self.destroy,
               padding=10).pack(side="left")
        button_frame.pack(side="bottom")

    def click_today(self):
        """
        Mark the habit as completed for today and update the main window.

        Raises:
            AttributeError: Main window has no attribute selected habit id.
            AttributeError: Main window has no attribute load habits or all habits.
        """
        try:
            habit = Analytics.get_marked_completed(\
                habit_id=self.main_window.center_frame.selected_habit_id.get())
        except AttributeError as exc:
            self.destroy()
            raise AttributeError("Main window has no attribute selected habit id."
                                ) from exc
        habit.save()
        try:
            self.main_window.analytics.all_habits = Analytics.load_habits()
            self.main_window.reload_center_frame(self.main_window.analytics.all_habits)
        except AttributeError as exc:
            self.destroy()
            raise AttributeError("Main window has no attribute load habits or all habits."
                                ) from exc
        self.destroy()

    def click_date(self):
        """
        Mark the habit as completed for the selected date and update the main window.

        Raises:
            AttributeError: Main window has no attribute selected habit id.
            AttributeError: Main window has no attribute load habits or all habits.

        """
        date_str = self.calendar.get_date()
        month, day, year = [int(date_) for date_ in date_str.split("/")]
        year = 2000 + year
        try:
            habit = Analytics.get_marked_completed(\
                habit_id=self.main_window.center_frame.selected_habit_id.get(),
                date=date(year=year,month=month,day=day)
                )
        except AttributeError as exc:
            self.destroy()
            raise AttributeError("Main window has no attribute selected habit id."
                                ) from exc
        habit.save()
        try:
            self.main_window.analytics.all_habits = Analytics.load_habits()
            self.main_window.reload_center_frame(self.main_window.analytics.all_habits)
        except AttributeError as exc:
            self.destroy()
            raise AttributeError("Main window has no attribute load habits or all habits."
                                ) from exc
        self.destroy()


class PopUpCalendar(PopUpWindow):
    """
        Initialize a pop-up calendar window that displays a calendar
        with completed dates highlighted.
        
        Args:
            main_window (Tk): The main application window.
            completed_dates (list, optional):
                A list of dates that have been completed. Default to None.
            frequency (int, optional): The frequency of the habit. Default to 1.

        Raises:
            TypeError: Frequency must be integer.
        """
    def __init__(self, main_window, completed_dates=None, frequency=1):
        super().__init__(main_window)

        self.frequency=frequency
        if not isinstance(frequency, int):
            raise TypeError("Frequency must be integer.")

        self.completed_dates = completed_dates
        if completed_dates is None:
            self.completed_dates=[]

        self.title("completed dates")
        self.calendar = Calendar(master=self, selectmode="day")
        self.calendar.pack()
        self.check_dates(completed_dates=self.completed_dates, frequency=self.frequency)

    def check_dates(self,completed_dates,frequency):
        """
        Highlight the completed dates on the calendar.
        
        Args:
            completed_dates (list): A list of dates that have been completed.
            frequency (int): The frequency of the habit.

        Raises:
            TypeError: Completed dates is not iterable.
        """
        try:
            for completed in completed_dates:
                for i in range(frequency):
                    #dates have to be datime.date type to be shown in the calendar
                    if isinstance(completed,date):
                        if i==0:
                            #set backgroundcolor of the first day of a period to green
                            self.calendar.calevent_create(date=completed+timedelta(days=i),
                                                text='Hello World', tags= "Day one")
                            self.calendar.tag_config("Day one", background='green',
                                                     foreground='white')
                        else:
                            #set backgroundcolor of the other days of a period to lightgreen
                            self.calendar.calevent_create(date=completed+timedelta(days=i),
                                                    text='Hello World', tags= "The other days")
                            self.calendar.tag_config("The other days", background="#49cc6c",
                                                    foreground='white')
        except TypeError as exc:
            self.destroy()
            raise TypeError("Completed dates is not iterable.") from exc

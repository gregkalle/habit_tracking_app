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
from datetime import date, datetime, timedelta
from tkcalendar import Calendar
from scr.pop_up_window import PopUpWindow
import scr.analytics as ana
from scr.habit import Habit

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

    Raises: ValueError: Behave must be BEHAVE_NEW_HABIT or BEHAVE_CHANGE_HABIT

    """

    BEHAVE_NEW_HABIT = "new habit"
    BEHAVE_CHANGE_HABIT = "change habit"


    def __init__(self, main_window, habit_id, behave = BEHAVE_NEW_HABIT):
        super().__init__(main_window=main_window,habit_id=habit_id)

        #If behave is "new habit", a "new habit"-window is created,
        #if behave is "change habit", a "change habit"-window is created.
        self.behave = behave
        if (self.behave == EntryPopUp.BEHAVE_NEW_HABIT and
               self.behave ==EntryPopUp.BEHAVE_CHANGE_HABIT):
            raise ValueError("Behave must be BEHAVE_NEW_HABIT or BEHAVE_CHANGE_HABIT")
        self.title(self.behave)

        self.habit_frequency = tk.IntVar(self)

        #pack habit name entry field
        self.entry_habit_name = self.pack_name_entry_field(label_text="habit name")
        #pack habit description entry field
        self.entry_habit_description = self.pack_name_entry_field(label_text="habit description")

        if self.behave == EntryPopUp.BEHAVE_NEW_HABIT:
            #pack  frequency entry field
            self.pack_frequency_entry_field(label_text="frequency",variable=self.habit_frequency)
        #create and pack the buttons of the entry window
        self.pack_buttons()


    def pack_name_entry_field(self, label_text):
        """
        Pack label and entry field and return the entry field.
        
        Args:
            label_text (str): The text of the label.
        
        Returns:
            ttk.Entry: The entry field widget.
        """
        frame = ttk.Frame(self)
        #create and pack the label to the frame
        ttk.Label(frame,anchor="w",text=label_text,padding=10).pack(side="left")
        #create the entry field
        textbox = ttk.Entry(frame)
        #pack the entry field to the frame
        textbox.pack(side="left")
        #pack the frame to the entry window
        frame.pack()
        #return entryfield
        return textbox

    def pack_frequency_entry_field(self, label_text, variable):
        """
        Pack label and radio buttons for frequency selection.
        
        Args:
            label_text (str): The text of the label.
            variable (tk.IntVar): The variable to store the selected frequency.

        Raises:
            AttributeError: Main window has no attribut USABLE_FREQUENCIES
        """
        frame = ttk.Frame(self)
        ttk.Label(frame,anchor="w",text=label_text,padding=10).pack(side="left")
        try:
            #create the radiobutton to select the frequency
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
        #Habit must have a name, description or frequency
        if not (self.entry_habit_name.get() and self.entry_habit_description.get()\
                and self.habit_frequency.get()):
            #error message, if one property is empty.
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="""The name and description of your habit may not be
                        empty and you must select a frequency"""
                       )
            message.show()
        else:
            #creat new habit and save it to the database
            habit = Habit(name=self.entry_habit_name.get(),
                         description=self.entry_habit_description.get(),
                         frequency=self.habit_frequency.get())
            habit.save()
            try:
                #append the list all_habits of the main window
                self.main_window.all_habits.append(habit)
            except AttributeError as exc:
                self.destroy()
                raise AttributeError("Main window has no attribute all_habits"
                                     ) from exc


            try:
                #reload the center_frame of the main window
                self.main_window.reload_center_frame(self.main_window.all_habits)
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
        #Habit must have a name or description
        if not (self.entry_habit_name.get() or self.entry_habit_description.get()):
            #error message, if one property is empty.
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                       message="The name and description of your habit may not be empty",
                       )
            message.show()
        else:
            try:
                #change the name or the description of the habit
                habit = Habit.change_habit_name_description\
                    (habit_id=self.habit_id,
                    habit_name=self.entry_habit_name.get(),
                    habit_description=self.entry_habit_description.get())
            except AttributeError as exc:
                self.destroy()
                raise AttributeError("""Main window has no attribute center frame
                                     or selected habid id.""") from exc
            #save changes to database
            habit.save()
            try:
                #reload all_habits
                self.main_window.all_habits=Habit.load_all()
                #reload the center_frame
                self.main_window.reload_center_frame(self.main_window.all_habits)
            except AttributeError as exc:
                self.destroy()
                raise AttributeError("""Main window has no attribute load habits or
                                    all habits.""") from exc
        self.destroy()


class DatePicker(PopUpWindow):

    """
    A pop-up window for selecting dates using a calendar widget.

    Args:
        main_window (tkinter.Tk): The main application window.
    """

    def __init__(self, main_window, habit_id):
        super().__init__(main_window=main_window,habit_id=habit_id)

        self.title("select date")
        self.calendar = Calendar(master=self, selectmode="day")
        self.calendar.pack()
        self.pack_buttons()

    def pack_buttons(self):
        """
        Create and pack the buttons for the date picker window.
        """
        button_frame = ttk.Frame(self)
        ttk.Button(button_frame, text="today", command=self.mark_date,
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
        self.mark_date()

    def click_date(self):
        """
        Transforms the date input of the datepicker in datetime.date
        format and call th mark_date method.

        Raises:
            AttributeError: Main window has no attribute selected habit id.
            AttributeError: Main window has no attribute load habits or all habits.

        """
        date_str = self.calendar.get_date()
        #split and save the picked date in month, day and year
        month, day, year = [int(date_) for date_ in date_str.split("/")]
        #add 2000 to year becaus it is given as YY
        year = 2000 + year
        #create date as datetime day type and call mark_date method
        self.mark_date(checked_date=date(year=year,month=month,day=day))

    def mark_date(self,checked_date=date.today()):

        """
        Mark the habit as completed for the checked_date and update the main window.

        Raises:
            AttributeError: Main window has no attribute selected habit id.
            AttributeError: Main window has no attribute load habits or all habits.
        """
        
        try:
            habit = ana.get_current_tracked_habit(
                habit_id=self.habit_id,
                habit_list=self.main_window.all_habits
                )
            #mark the habit as fulfilled the selected day
            habit.completion.mark_completed(checked_date=checked_date)
        except AttributeError as exc:
            self.destroy()
            raise AttributeError("Main window has no attribute selected habit id."
                                ) from exc
        except ValueError:
            #shows error message if picked date not between createn date and today.
            message = mb.Message(self,icon=mb.ERROR,type=mb.OK,title="INPUT ERROR",
                            message="Selected date must be between "\
                                f"{habit["creation_time"].strftime('%d.%m.%Y')} "\
                                f"and {datetime.now().strftime('%d.%m.%Y')}."
                            )
            message.show()
        else:
            #save changes
            habit.save()
            try:
                #reload all_habits and center frame of main window
                self.main_window.all_habits = Habit.load_all()
                self.main_window.reload_center_frame(self.main_window.all_habits)
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
                A list of dates that have been completed. Default is None.
            frequency (int, optional): The frequency of the habit. Default is 1.
            creation_date: The date the habit is created. Default is datetime.date.today().

        Raises:
            TypeError: Frequency must be integer.
            TypeError: Creation date must be of type datetime.date.
            TypeError: Completed dates must be list or None.
        """
    def __init__(self, main_window, completed_dates=None, frequency=1, creation_date = date.today):
        super().__init__(main_window=main_window)

        if not isinstance(frequency, int):
            raise TypeError("Frequency must be integer.")
        if not isinstance(creation_date, date):
            raise TypeError("Creation date must be of type datetime.date.")
        if not isinstance(completed_dates, list) and not completed_dates is None:
            raise TypeError("Completed dates must be list or None.")

        self.frequency=frequency
        self.completed_dates = completed_dates
        if completed_dates is None:
            self.completed_dates = []
        self.creation_date = creation_date

        self.geometry("300x200")
        self.title("completed dates")
        self.calendar = Calendar(master=self, selectmode="day")
        self.calendar.pack()
        self.check_dates(completed_dates=self.completed_dates,
                         frequency=self.frequency,
                         creation_date=self.creation_date)

    def check_dates(self,completed_dates,frequency,creation_date):
        """
        Highlight the completed dates on the calendar.
        
        Args:
            completed_dates (list): A list of dates that have been completed.
            frequency (int): The frequency of the habit.

        Raises:
            TypeError: Completed dates is not iterable.
        """
        #set beckgroundcolor for the creation day to red
        self.calendar.calevent_create(date=creation_date,text="Calendar",
                                      tags= "Creation date")
        self.calendar.tag_config("Creation date", background="red",
                                foreground="white")
        try:
            for completed in completed_dates:
                for i in range(frequency):
                    #dates have to be datime.date type to be shown in the calendar
                    if isinstance(completed,date):
                        if i==0:
                            if completed == creation_date:
                                #set foreground color of the creation day to green if it is checked
                                self.calendar.calevent_create(date=completed+timedelta(days=i),
                                                    text="Calendar",
                                                    tags= "Day one equal creation date")
                                self.calendar.tag_config("Day one equal creation date",
                                                        background="red",
                                                        foreground="green")
                            else:
                            #set backgroundcolor of the first day of a period to green
                                self.calendar.calevent_create(date=completed+timedelta(days=i),
                                                    text="Calendar", tags= "Day one")
                                self.calendar.tag_config("Day one", background="green",
                                                        foreground="white")
                        else:
                            #set backgroundcolor of the other days of a period to lightgreen
                            self.calendar.calevent_create(date=completed+timedelta(days=i),
                                                    text="Calendar", tags= "The other days")
                            self.calendar.tag_config("The other days", background="#49cc6c",
                                                    foreground="white")
        except TypeError as exc:
            self.destroy()
            raise TypeError("Completed dates is not iterable.") from exc

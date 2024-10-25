from tkinter import Tk
from tkinter.ttk import Frame, Button
from datetime import date, timedelta
from tkcalendar import Calendar
from scr.analytics import Analytics

class PopUpWindow(Tk):

    """
    A base class for creating pop-up windows.
    
    Attributes:
        main_window (Tk): The main application window.
    """

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.main_window.add_child_window(self)


    def destroy(self):
        """
        Override the destroy method to remove the child window reference from the main window.
        """
        try:
            self.main_window.remove_child_window(self)
        except AttributeError as exc:
            raise AttributeError("Mai window has no attribut remove_child_window") from exc
        return super().destroy()


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
        button_frame = Frame(self)
        Button(button_frame, text="today", command=self.click_today,
               padding=10).pack(side="left")
        Button(button_frame, text="select date", command=self.click_date,
               padding=10).pack(side="left")
        Button(button_frame, text="Cancel", command=self.destroy,
               padding=10).pack(side="left")
        button_frame.pack(side="bottom")

    def click_today(self):
        """
        Mark the habit as completed for today and update the main window.
        """
        habit = Analytics.get_marked_completed(\
            habit_id=self.main_window.center_frame.selected_habit_id.get())
        habit.save()
        self.main_window.analytics.load_habits()
        self.main_window.reload_center_frame(self.main_window.analytics.all_habits)
        self.destroy()

    def click_date(self):
        """
        Mark the habit as completed for the selected date and update the main window.
        """
        date_str = self.calendar.get_date()
        month, day, year = [int(date_) for date_ in date_str.split("/")]
        year = 2000 + year
        habit = Analytics.get_marked_completed(\
            habit_id=self.main_window.center_frame.selected_habit_id.get(),
            date=date(year=year,month=month,day=day)
            )
        habit.save()
        self.main_window.analytics.load_habits()
        self.main_window.reload_center_frame(self.main_window.analytics.all_habits)
        self.destroy()


class PopUpCalendar(PopUpWindow):

    def __init__(self, main_window, completed_dates=None, frequency=1):
        super().__init__(main_window)

        self.title("completed dates")
        self.calendar = Calendar(master=self, selectmode="day")
        self.calendar.pack()
        self.completed_dates = completed_dates
        if completed_dates is None:
            self.completed_dates=[]
        self.frequency=frequency
        self.check_dates(completed_dates=self.completed_dates, frequency=self.frequency)

    def check_dates(self,completed_dates,frequency):
        for completed in completed_dates:
            for i in range(frequency):
                self.calendar.calevent_create(date=completed+timedelta(days=i),
                                              text='Hello World', tags= "Message")
                self.calendar.tag_config("Message", background='green', foreground='white')

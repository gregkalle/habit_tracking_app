
"""
NAME
    completion

DESCRIPTION
    Processes the habit data.

CLASSES
    Completion
"""
from datetime import  datetime, date, timedelta

class Completion:
    """
    Processes the habit data.

    Args:
        frequency (int):
        completed_dates (list):
        creation_time (datetime.datetime):

    Attributes:
        WEEKLY (int): The frequency for a weekly habit. Is set to 7.
        Daily (int): The frequency for a daily habit. Is set to 1.
        self["frequency"] (int): The frequency of the complition
        self["completed_dates"] (list): The list of the completed dates.
        self["creation_time"] (datetime): The datetime when the completion is created.

    Raises:
        ValueError: Frequency must be a positiv integer.
        TypeError: Creation time must be of type datetime.datetime.
        TypeError: The elements of completed dates must be of type datetime.date.
    """
    WEEKLY = 7
    DAILY = 1

    def __init__(self, frequency = DAILY, completed_dates = None, creation_time = None):
        #checkes if the frequency a positiv integer
        if not isinstance(frequency, int) or frequency < Completion.DAILY:
            raise ValueError("Frequency must be a positiv integer.")

        #set default completed_dates
        if completed_dates is None:
            completed_dates=[]

        #checks if completed dates is list, and if not creats a list
        if not isinstance(completed_dates,list):
            completed_dates = [completed_dates]

        #sets creation time to now if not seted and check if o type datetime.
        if not creation_time:
            creation_time = datetime.now()
        if not isinstance(creation_time,datetime):
            raise TypeError("Creation time must be of type datetime.datetime.")

        #checks if all elements are the type datetime.date and raises error if not.
        for element in completed_dates:
            if not isinstance(element,date) or isinstance(element,datetime):
                raise TypeError("The elements of completed dates must be of type datetime.date.")

        #set the properties of the class to a dictonary
        self.record = {"frequency": frequency,
                  "completed_dates": completed_dates,
                  "creation_time": creation_time}

    #set the __getitem__ function that the properties are callable with self["property"]
    def __getitem__(self, name):
        return self.record[name]

    def mark_completed(self, checked_date=None):
        """
        The habit is been completed today or at a special date.
        Works only if date between creation date and today.

        Args:
            checked_date (datetime.date): The date of the day on which the habit is been completed.
                                          Default is datetime.date.today().
        Raise:
            TypeError: The checked date must be of type datetime.date.
            ValueError: Checked date is out of checkable intervall.
        """
        #set default cecked date to the date today
        if checked_date is None:
            checked_date = date.today()

        #checks if date is of type datetime.date and raises error if not.
        if not isinstance(checked_date,date) or isinstance(checked_date,datetime):
            raise TypeError("The checked date must be of type datetime.date.")
        
        #if checked date before creation time, no date will be marked completed.
        if checked_date < self.record["creation_time"].date() or\
           checked_date > date.today():
            raise ValueError("Checked date is out of checkable intervall.")

        # set the checked date to the start date of the periode
        checked_date = checked_date\
            - (checked_date-self.record["creation_time"].date())\
            %timedelta(days=self.record["frequency"])

        #append completed_dates only if checked_date is a new date
        if checked_date not in self.record["completed_dates"]:
            self.record["completed_dates"].append(checked_date)


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
        frequency (int):The periodicity of the habit. Default is DAILY.
        completed_dates (list): List of the completed dates. Default is None.
        creation_time (datetime.datetime): The time when the habit is created.
                                           Default is datetime.datetime.now().

    Raises:
        ValueError: Frequency must be a positiv integer.
    """
    WEEKLY = 7
    """ WEEKLY is set to 7"""
    DAILY = 1
    """DAILY is set to 1"""

    def __init__(self, frequency = DAILY, completed_dates = None, creation_time = None):
        if not isinstance(frequency, int) or frequency < Completion.DAILY:
            raise ValueError("Frequency must be a positiv integer.")
        if completed_dates is None:
            completed_dates=[]
        if not isinstance(completed_dates,list):
            completed_dates = [completed_dates]
        if not creation_time:
            creation_time = datetime.now()
        for date_ in completed_dates:
            Completion.validate_date(date_)
        self.record = {"frequency": frequency,
                  "completed_dates": completed_dates,
                  "creation_time": creation_time}

    def __getitem__(self, name):
        return self.record[name]

    def mark_completed(self, checked_date=None):
        """
        The habit is been completed today or at a special date.

        Args:
            checked_date (datetime.date): The date of the day on which the habit is been completed.
                                          Default is datetime.date.today().
        """
        if checked_date is None:
            checked_date = date.today()

        Completion.validate_date(checked_date)
        # set the checked date to the next periode
        checked_date = checked_date\
            - (checked_date-self.record["creation_time"].date())\
            %timedelta(days=self.record["frequency"])

        if checked_date not in self.record["completed_dates"]:
            self.record["completed_dates"].append(checked_date)

    @classmethod
    def validate_date(cls, validation_data):
        """
        Validates the type of the data and raises an error if not of type datetime.date.

        Args:
            validation_data (datetime.date): The data which should be validated.
        
        Raises:
            TypeError: The data must be of type datetime.date.
        """
        if not isinstance(validation_data,date) or isinstance(validation_data,datetime):
            raise TypeError("The data must be of type datetime.date.")

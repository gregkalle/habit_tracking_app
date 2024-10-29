
"""
NAME
    completion

DESCRIPTION
    Processes the habit data.

CLASSES
    Completion
"""
from datetime import  datetime, date, timedelta
from math import ceil

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
        if not isinstance(frequency, int) and frequency < Completion.DAILY:
            raise ValueError("Frequency must be a positiv integer.")
        self.frequency = frequency
        self.completed_dates = completed_dates
        if self.completed_dates is None:
            self.completed_dates=[]
        self.creation_time = creation_time
        if not creation_time:
            self.creation_time = datetime.now()
        for date_ in self.completed_dates:
            self.validate_date(date_)


    def mark_completed(self, checked_date=None):
        """
        The habit is been completed today or at a special date.

        Args:
            checked_date (datetime.date): The date of the day on which the habit is been completed.
                                          Default is datetime.date.today().
        """
        if checked_date is None:
            checked_date = date.today()

        self.validate_date(checked_date)
        # set the checked date to the next periode
        checked_date = self.creation_time.date() \
            + timedelta(ceil((checked_date - self.creation_time.date()\
                              ).days/self.frequency) * self.frequency)

        if checked_date not in self.completed_dates:
            self.completed_dates.append(checked_date)


    def calculate_streak(self):
        """
        Calculate the actuell streak count.

        Returns:
            int: The number of consecutive periods the habit was fulfilled included today.
        """
        today = date.today()
        today = self.creation_time.date() +\
            timedelta(ceil((today - self.creation_time.date()).days/self.frequency)\
                      * self.frequency)
        streak = 0
        while today in self.completed_dates:
            streak += 1
            today -= timedelta(days=self.frequency)
        return streak

    def calculate_longest_streak(self):
        """
        Calculate the longest streak count.

        Returns:
            int: The highest number of consecutive periods the habit was fulfilled.
        """
        if not self.completed_dates:
            return 0

        longest_streak = 1
        streak = 1
        self.completed_dates.sort()
        for i in range(1,len(self.completed_dates)):
            if self.completed_dates[i] ==\
                  self.completed_dates[i-1] +timedelta(days=self.frequency):
                streak += 1
            else:
                streak = 1
            longest_streak = max(streak, longest_streak)
        return longest_streak

    def validate_date(self, validation_data):
        """
        Validates the type of the data and raises an error if not of type datetime.date.

        Args:
            validation_data (datetime.date): The data which should be validated.
        
        Raises:
            TypeError: The data must be of type datetime.date.
        """
        if not isinstance(validation_data,date):
            raise TypeError("The data must be of type datetime.date.")

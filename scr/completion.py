from datetime import  datetime, date, timedelta
from math import ceil

class Completion:
    """Have you completed the habit today or not"""
    WEEKLY = 7
    """ WEEKLY is set to 7"""
    DAILY = 1
    """DAILY is set to 1"""

    def __init__(self, frequency = DAILY, completed_dates = [], creation_time = None):
        """Attributs:
        frequency (DAILY , WEEKLY)
        completed_dates
        """
        
        self.frequency = frequency
        self.completed_dates = completed_dates
        self.creation_time = creation_time
        if not creation_time:
            self.creation_time = datetime.now() 
        self.set_valid_dates()
        

    def mark_completed(self, checked_date=None):
        """the habit is checked today or at a special date"""
        if checked_date is None:
            checked_date = date.today()

        # set the checked date to the next periode      
        checked_date = self.creation_time.date() + timedelta(ceil((checked_date - self.creation_time.date()).days/self.frequency) * self.frequency)
        
        if checked_date not in self.completed_dates:
            self.completed_dates.append(checked_date)

    def calculate_streak(self):
        """the actual streak count"""
        today = date.today()
        streak = 0
        while today in self.completed_dates:
            streak += 1
            today -= timedelta(days=self.frequency)
        return streak
            
    def calculate_longest_streak(self):
        """calculate the longest streak"""
        self.set_valid_dates()
        if not self.completed_dates:
            return 0
            
        longest_streak = 1
        streak = 1
        self.completed_dates.sort()
        for i in range(1,len(self.completed_dates)):
            if self.completed_dates[i] == self.completed_dates[i-1] + timedelta(days=self.frequency):
                streak += 1
            else:
                streak = 1
            longest_streak = max(streak, longest_streak)
        return longest_streak

    def set_valid_dates(self):
        """
        
        """
        self.completed_dates = [d for d in self.completed_dates if isinstance(d,date)]
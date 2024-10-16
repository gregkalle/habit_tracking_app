from scr.sqlite_storage import SQLiteStorage
from scr.completion import Completion


class Habit():
    """

    
    """
    DEFAULT_STORAGE_STRATEGY = SQLiteStorage()
    
    def __init__(self, name="new habit", description="new description", frequency = Completion.DAILY, completed_dates=[], habit_id=None):
        """
        
        """
        self.completion = Completion(frequency, completed_dates)
        self.name = name
        self.description = description
        self.habit_id = habit_id

    def save(self):
        """save the habit into the database"""
        Habit.DEFAULT_STORAGE_STRATEGY.save(self)

    @classmethod
    def load(cls, habit_id):
        """load a habit from the database"""
        
        data = cls.DEFAULT_STORAGE_STRATEGY.load(habit_id)
        if not data:
            return None
        
        return Habit(frequency=data["frequency"], completed_dates=data["completed_dates"],
                     name=data["name"], description=data["description"], habit_id=data["habit_id"])
    
    @classmethod
    def load_all(cls):
        """load all habits from the database"""
        all_id = cls.DEFAULT_STORAGE_STRATEGY.get_all_id()
        return[cls.load(habit_id) for habit_id in all_id]

    @classmethod
    def delete(cls, habit_id):
        """delete a habit in the database"""
        cls.DEFAULT_STORAGE_STRATEGY.delete(habit_id)
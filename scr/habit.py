
"""
NAME
    habit

DESCRIPTION
    Contains the habit class

CLASSES
    Habit
"""
from scr.sqlite_storage import SQLiteStorage
from scr.completion import Completion


class Habit():
    """
    The habit class

    Args:
        name (str): The name of the habit
        description (str): The description of the habit
        frequency (int): The periodicity of the habit. Default is Completion.DAILY.
        completed_dates (list): List of the completed dates. Default is None.
        creation_time (datetime.datetime): The time when the habit is created. Default is None.
        habit_id (int): The id with which is the habit stored in the database. Default is None.

    Attributes:
        DEFAULT_STORAGE_STRATEGY (SQLiteStorge): The strategy which saves
                                                and loads habits to the database
        name (str): The name of the habit.
        description (str): The description of the habit.
        habit_id (int): The id with which is the habit stored in the database.
        completion (Completion): Class which processes the habit data.  
    """
    DEFAULT_STORAGE_STRATEGY = SQLiteStorage()

    def __init__(self, name, description, frequency = Completion.DAILY,
                 completed_dates=None, creation_time = None, habit_id=None):

        self.completion = Completion(frequency, completed_dates, creation_time)
        self.name = name or "new habit"
        self.description = description or "new description"
        self.habit_id = habit_id

    def __eq__(self, habit):
        if isinstance(habit,Habit) and habit.name == self.name\
                                   and habit.description == self.description\
                                   and habit.habit_id == self.habit_id:
            return True
        return False

    def save(self):
        """
        Save the habit into the database

        Raises:
            TypeError: Habit is not savable.
        """
        try:
            Habit.DEFAULT_STORAGE_STRATEGY.save(self)
        except TypeError as exc:
            raise TypeError("Habit is not savable.")from exc

    @classmethod
    def load(cls, habit_id):
        """
        Load the habit from the database
        
        Args:
            habit_id (int): The id with which is the habit stored in the database.

        Returns:
            Habit: The habit with the habit_id if existing.
        """

        data = cls.DEFAULT_STORAGE_STRATEGY.load(habit_id)

        if not data:
            return None

        return Habit(frequency=data["frequency"], completed_dates=data["completed_dates"],
                     name=data["name"], description=data["description"],
                     creation_time=data["creation_time"], habit_id=data["habit_id"])

    @classmethod
    def load_all(cls):
        """
        Load all habits from the database
        
        Returns:
            [Habit]: A List of all habits stored in the database.
        """
        all_id = cls.DEFAULT_STORAGE_STRATEGY.get_all_id()
        return [cls.load(habit_id) for habit_id in all_id]

    @classmethod
    def delete(cls, habit_id):
        """
        Delete a habit with the id in the database

        Args:
            habit_id (int): The id with which is the habit stored in the database.
        """
        try:
            cls.DEFAULT_STORAGE_STRATEGY.delete(habit_id)
        except ValueError as exc:
            raise ValueError("ID is not in database.") from exc

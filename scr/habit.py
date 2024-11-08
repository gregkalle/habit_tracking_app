"""
NAME
    habit

DESCRIPTION
    Contains the habit class

CLASSES
    Habit
"""
import scr.analytics as ana
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

    def __init__(self, name, description, habit_id=None, frequency = Completion.DAILY,
                 completed_dates=None, creation_time = None):

        self.completion = Completion(frequency, completed_dates, creation_time)
        name = name or "new habit"
        description = description or "new description"
        self.__record = {"name": name,
                  "description": description,
                  "habit_id": habit_id
                  }

    def __eq__(self, habit):
        if isinstance(habit,Habit) and habit["name"] == self["name"]\
                                   and habit["description"] == self["description"]\
                                   and habit["habit_id"] == self["habit_id"]:
            return True
        return NotImplemented

    def __getitem__(self,name):
        if name in self.completion.record:
            return self.completion[name]
        return self.__record[name]

    def __setitem__(self, name, value):
        self.__record[name]=value

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

        Raises:
            ValueError: ID is not in database.
        """
        try:
            cls.DEFAULT_STORAGE_STRATEGY.delete(habit_id)
        except ValueError as exc:
            raise ValueError("ID is not in database.") from exc

    @classmethod
    def change_habit_name_description(cls, habit_id, habit_name=None, habit_description=None):
        """
        Changes the name or the description of the habit with given id.

        Args:
            habit_id (int): The id of the habit which should be changed.
            habit_name (str): The new name of the habit. Default is None.
            habit_description (str): The new description of the habit. Default is None.

        Returns:
            Habit: The habit with changed name or description.

        Raises:
            ValueError: There is no habit with habit id in the database.
        """
        habit = Habit.load(habit_id=habit_id)
        if not habit:
            raise ValueError(f"There is no habit with id {habit_id} in the database.")
        if habit_name:
            habit["name"] = habit_name
        if habit_description:
            habit["description"] = habit_description
        return habit

    @classmethod
    def habit_data(cls, habit):
        """
        Returns the habit data as a tuple.

        Returns:
            (habit_id (int), habit_name (str), description (str),
            frequency (int), current_streak (int), longest_streak (int)

        Raises:
            TypeError: "Object not of type Habit.
        """
        #check if habit of type Habit
        if not isinstance(habit,Habit):
            raise TypeError("Object not of type Habit.")

        return (habit["habit_id"],
                habit["name"],
                habit["description"],
                habit["frequency"],
                ana.get_current_streak(habit=habit),
                ana.get_longest_streak(habit=habit))

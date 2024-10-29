"""
NAME
    analytics

DESCRIPTION
    Connects the habit modul an an user interface.

CLASSES
    Analytics
"""
from scr.habit import Habit

class Analytics:
    """
    Connection class between the habit and the habit data an an user interface(UI).

    Attributes:
        MIN_DEFAULT_HABIT (int): The minimal number of habits shown in the UI.
        HABIT_LIST_TITLES (list): The keys of the dictionary which returns the habit data.
        all_habits (list): The list of all habits stored in the database.
    """

    MIN_DEFAULT_HABIT = 5
    HABIT_LIST_TITLES = ["selected", "habit name", "description", "frequency",
                         "current streak", "longest streak"]


    def __init__(self):
        self.all_habits = Analytics.load_habits()

        # creating the missing amount of habits to the MIN_DEFAULT_HABIT value
        if len(self.all_habits) < Analytics.MIN_DEFAULT_HABIT:
            for i in range(Analytics.MIN_DEFAULT_HABIT - len(self.all_habits)):
                habit = Habit(name = f"Default habit name {i}",
                              description=f"Default habit description {i}")
                habit.save()
                self.all_habits.append(habit)

    @classmethod
    def load_habits(cls):
        """
        Load all habits.

        Returns:
            [Habit]: List of all habits stored in the database.
        """
        return Habit.load_all()


    @classmethod
    def get_current_tracked_habit(cls, habit_id):
        """
        Returns the habit with id.

        Args:
            habit_id (int): The id with which is the habit stored in the database.

        Returns:
            Habit: The habit with the habit_id if existing.

        Raises:
            ValueError: "There is no habit with id habit_id in the database."
        """
        habit = Habit.load(habit_id=habit_id)
        if not habit:
            raise ValueError(f"There is no habit with id {habit_id} in the database.")
        return habit

    @classmethod
    def get_habits_with_frequency(cls, habit_list, frequency):
        """
        Get all habit with the seted periodicity.

        Args:
            habit_list (list): The list of habits which should be checked.
            frequency (int): The periodicity of the habits.

        Returns:
            [Habit]: The list of habits with seted periodicity.

        Raises:
            TypeError: Frequency not of type integer.
            TypeError: Object not of type Habit.
        """
        #Check if frequency of type integer
        if not isinstance(frequency, int):
            raise TypeError("Frequency not of type integer.")
        #Check if all elements of habit_list are of type Habit
        if not all(list(map(lambda x: isinstance(x,Habit), habit_list))):
            raise TypeError("Object not of type Habit.")
        return [habit for habit in habit_list if habit.completion.frequency == frequency]

    @classmethod
    def get_all_longest_streaks(cls, habit_list):
        """
        Get the longest streaks of the habits in the habit list.

        Args:
            habit_list (list): The list of habits from which
                        the longest series should be calculated.

        Returns:
            {int: int}: The habit_id as key and the longest streak as value of a dictonary

        Raises:
            TypeError: Object not of type Habit.
        """
        #Check if all elements of habit_list are of type Habit
        if not all(list(map(lambda x: isinstance(x,Habit), habit_list))):
            raise TypeError("Object not of type Habit.")
        return {habit.habit_id : habit.completion.calculate_longest_streak()
                for habit in habit_list}

    @classmethod
    def get_longest_streak(cls, habit):
        """
        Get the longest streak of habit.

        Args:
            habit(Habit): The habits from which the longest series should be calculated

        Returns:
            int: The value of the longest streak.

        Raises:
            TypeError: Object not of type Habit.
        """
        #check if habit of type Habit
        if not isinstance(habit,Habit):
            raise TypeError("Object not of type Habit.")
        return habit.completion.calculate_longest_streak()

    @classmethod
    def get_all_current_streaks(cls, habit_list):
        """
        Get the current streaks of the habits in the habit list.

        Args:
            habit_list (list): The list of habits from which
                        the current series should be calculated.

        Returns:
            {int: int}: The habit_id as key and the current streak as value of a dictonary

        Raises:
            TypeError: Object not of type Habit.
        """
        #Check if all elements of habit_list are of type Habit
        if not all(list(map(lambda x: isinstance(x,Habit), habit_list))):
            raise TypeError("Object not of type Habit.")
        return {habit.habit_id : habit.completion.calculate_streak() for habit in habit_list}

    @classmethod
    def get_current_streak(cls, habit):
        """
        Get the current streak of habit.

        Args:
            habit(Habit): The habits from which the current series should be calculated

        Returns:
            int: The value of the current streak.

        Raises:
            TypeError: Object not of type Habit.
        """
        #check if habit of type Habit
        if not isinstance(habit,Habit):
            raise TypeError("Object not of type Habit.")
        return habit.completion.calculate_streak()

    @classmethod
    def habit_to_dict(cls, habit):
        """
        Returns the habit data as a dictionary.

        Returns:
            {"selected" : habit_id (int),
            "habit name" : habit_name (str),
            "description" : description (str),
            "frequency" : frequency (int),
            "current streak" : current_streak (int),
            "longest streak" : longest_streak (int)}

        Raises:
            TypeError: "Object not of type Habit.
        """
        #check if habit of type Habit
        if not isinstance(habit,Habit):
            raise TypeError("Object not of type Habit.")
        return {cls.HABIT_LIST_TITLES[0] : habit.habit_id, cls.HABIT_LIST_TITLES[1] : habit.name,
                cls.HABIT_LIST_TITLES[2] : habit.description,
                cls.HABIT_LIST_TITLES[3] : habit.completion.frequency,
                cls.HABIT_LIST_TITLES[4] : cls.get_current_streak(habit),
                cls.HABIT_LIST_TITLES[5] : cls.get_longest_streak(habit)
                }

    @classmethod
    def is_date_completed(cls, habit, date):
        """
        Checkes if the habit is completed at a given date.

        Args:
            habit (Habit): The habits which will be checked.
            date (datetime.date): The date which will be checked.

        Returns:
            bool: True if habit at date completed, else False.

        Raises:
            TypeError: Object not of type Habit.
        """
        #check if habit of type Habit
        if not isinstance(habit,Habit):
            raise TypeError("Object not of type Habit.")
        return date in habit.completion.completed_dates

    @classmethod
    def get_habit_ids(cls, habit_list):
        """
        Returns a list of the habit id.

        Args:
            habit_list (list): List of the habits from which the id should be returned.

        Returns:
            [int]: List of the ids of the habit.

        Raises:
            TypeError: Object not of type Habit.
        """
        #Check if all elements of habit_list are of type Habit
        if not all(list(map(lambda x: isinstance(x,Habit), habit_list))):
            raise TypeError("Object not of type Habit.")
        return [habit.habit_id for habit in habit_list]

    @classmethod
    def create_new_habit(cls, habit_name, habit_description, frequency):
        """
        Creates and returns new habit.

        Args:
            habit_name (str): The name of the new habit. If not of type string it is
                              seted to default habit name.
            habit_description (str): The description of the new habit.
                    If not of type string it is seted to default habit description.
            frequency (int): The new habits periodicity. If not of type integer it is
                             seted to default frequency.

        Returns:
            Habit: The new habit.
        """
        #check if habit_name and habit_description is a string and
        #frequency is an integer esle set values to default.
        habit_name = habit_name if isinstance(habit_name,str) else None
        habit_description = habit_description if isinstance(habit_description,str) else None
        frequency = frequency if isinstance(frequency,int) else None

        habit = Habit(name=habit_name,description=habit_description,frequency=frequency)
        return habit

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
            habit.name = habit_name
        if habit_description:
            habit.description = habit_description
        return habit

    @classmethod
    def delete_habit(cls, habit_id):
        """
        Deletes the habit with the habit id from the database.

        Args:
            habit_id (int): The id of the habit which should be deleted.

        Raises:
            ValueError: There is no habit with habit id in the database.
        """
        habit = Habit.load(habit_id=habit_id)
        if not habit:
            raise ValueError(f"There is no habit with id {habit_id} in the database.")
        Habit.delete(habit_id=habit.habit_id)

    @classmethod
    def get_marked_completed(cls, habit_id, date=None):
        """
        Returns the habit with the added date.

        Args:
            habit_id (int): The id of the habit the date should be added.
            date (datetime.date): The date which should be added. Default is None.
        
        Returns:
            Habit: The habit with added date.

        Raises:
            ValueError: There is no habit with habit id in the database.
        """
        habit = Habit.load(habit_id=habit_id)
        if not habit:
            raise ValueError(f"There is no habit with id {habit_id} in the database.")
        habit.completion.mark_completed(checked_date=date)
        return habit

"""
NAME
    analytics

DESCRIPTION
    Modul which contains the functions in functional programming paradigm for
    the habit tracking app.
"""
from datetime import date, timedelta
#from scr.habit import Habit


def get_current_tracked_habit(habit_id:int,habit_list:list)->object:
    """
    Returns the habit with id.

    Args:
        habit_id (int): The id with which is the habit stored in the database.
        habit_list (ist): A list of habits.

    Returns:
        Habit: The habit from the habit_list with the habit_id if existing.

    Raises:
        ValueError: "There is no habit with id habit_id in the list."
    """
    print("check")
    for habit in habit_list:
        if habit["habit_id"] == habit_id:
            return habit
    raise ValueError(f"There is no habit with id {habit_id} in the list.")

def get_all_current_tracked_habits(habit_list:list, id_list:list)->list:
    """
    Returns a list of habits with the ids from the id list.

    Args:
        habit_list (ist): A list of habits.
        id_list (list): The ids of the habits.

    Returns:
        [Habit]: A list of habits from the habit_list with the ids.

    Raises:
        ValueError: "There is no habit with id habit_id in the list."
    """
    result = []
    for habit_id in id_list:
        try:
            value = get_current_tracked_habit(habit_id=habit_id,habit_list=habit_list)
        except ValueError as exc:
            raise ValueError(f"There is no habit with id {habit_id} in the habit list.") from exc
        result.append(value)
    return result

def get_habit_with_frequency(habit_list:list, frequency:int)->list:
    """
    Get all habit with the selected periodicity.

    Args:
        habit_list (list): The list of habits which should be checked.
        frequency (int): The periodicity of the habits.

    Returns:
        [Habit]: The list of habits with selected periodicity.
    Raises:
        TypeError: Object not of type Habit.
    """
    try:
        return [habit for habit in habit_list if habit["frequency"] == frequency]
    except (KeyError,TypeError) as exc:
        raise TypeError("Object not of type Habit.") from exc


def get_current_streak(habit)->int:
    """
    Calculate the actuell streak count.

    Returns:
        int: The number of consecutive periods the habit was fulfilled included today.

    Raises:
        TypeError: Creation time not of type datetime.datetime.
    """
    today = date.today()
    try:
        creation_day = habit["creation_time"].date()
    except AttributeError as exc:
        raise TypeError("Creation time not of type datetime.datetime.") from exc
    today = today - (today-creation_day)%timedelta(days=habit["frequency"])

    streak = 0
    while today in habit["completed_dates"]:
        streak += 1
        today -= timedelta(days=habit["frequency"])
    return streak

def get_longest_streak(habit)->int:
    """
    Get the longest streak of habit.

    Args:
        habit(Habit): The habit from which the longest series should be calculated

    Returns:
        int: The value of the longest streak.

    Raises:
        TypeError: Creation time not of type datetime.datetime.
    """
    streak, longest_streak = (0,0)
    today = date.today()
    try:
        creation_day = habit["creation_time"].date()
    except AttributeError as exc:
        raise TypeError("Creation time not of type datetime.datetime.") from exc
    today = today - (today-creation_day)%timedelta(days=habit["frequency"])

    while today >= habit["creation_time"].date():
        if today in habit["completed_dates"]:
            streak += 1
        else:
            streak = 0
        longest_streak = max(longest_streak,streak)
        today -= timedelta(days=habit["frequency"])
    return longest_streak

def get_longest_streak_of_all(habit_list:list)->int:
    """
    Get the longest streak of all habits.

    Args:
        habit_list (list): The habits from which the longest series should be calculated

    Returns:
        int: The value of the longest streak of all habits.
    """
    over_all_longest_streak = 0
    for habit in habit_list:
        try:
            longest_streak = get_longest_streak(habit=habit)
        except TypeError:
            continue
        over_all_longest_streak = max(over_all_longest_streak,longest_streak)
    return over_all_longest_streak

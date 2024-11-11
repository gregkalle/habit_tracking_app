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
        TypeError: "Habit list is not a list."
        TypeError: "Object not of type Habit."
        ValueError: "There is no habit with id habit_id in the list."
    
    """
    #check if habit_list a list.
    if not isinstance(habit_list,list):
        raise TypeError("Habit list is not a list.")
    for habit in habit_list:
        try:
            #returns the habit with habit_id
            if habit["habit_id"] == habit_id:
                return habit
        except (TypeError,KeyError) as exc:
            raise TypeError("Object not of type Habit.") from exc

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
        TypeError: "Id list is not a list."
        ValueError: "There is no habit with id habit_id in the list."
        TypeError: "Habit list is not a list of habits."
    """
    #checks if id_list is a list
    if not isinstance(id_list,list):
        raise TypeError("Id list is not a list")
    result = []
    for habit_id in id_list:
        try:
            #get the habit with id habit_id
            value = get_current_tracked_habit(habit_id=habit_id,habit_list=habit_list)
        except ValueError as exc:
            raise ValueError(f"There is no habit with id {habit_id} in the habit list.") from exc
        except TypeError as exc:
            raise TypeError("Habit list is not a list of habits.") from exc
        #store habit in the esult list.
        result.append(value)
    return result

def get_habit_with_frequency(habit_list:list, frequency:int)->list:
    """
    Get all habit with the selected frequency.

    Args:
        habit_list (list): The list of habits which should be checked.
        frequency (int): The periodicity of the habits.

    Returns:
        [Habit]: The list of habits with selected periodicity.
    Raises:
        TypeError: "Habit list is not a list."
        TypeError: "Object not of type Habit."

    """
    if not isinstance(habit_list,list):
        raise TypeError("Habit list is not a list.")
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
        TypeError: Habit not of type Habit.
        TypeError: Creation time not of type datetime.datetime.
        TypeError: Completed dates is not iterable.
    """
    #check if habit keywords are callable.
    try:
        creation_time=habit["creation_time"]
        frequency=habit["frequency"]
        completed_dates=habit["completed_dates"]
    except (KeyError,TypeError) as exc:
        raise TypeError("Habit not of type Habit.") from exc

    #define today as the date from today
    today = date.today()
    try:
        #change creation_time of habit to date.
        creation_day = creation_time.date()
    except AttributeError as exc:
        raise TypeError("Creation time not of type datetime.datetime.") from exc

    #set today to the first day of the actuell period
    today = today - (today-creation_day)%timedelta(days=frequency)
    #initialise the streak count
    streak = 0

    try:
        while today in completed_dates:
            #count today to the streak
            streak += 1
            #set today to one day before today
            today -= timedelta(days=frequency)
    except TypeError as exc:
        raise TypeError("Completed dates is not iterable.") from exc

    return streak

def get_longest_streak(habit)->int:
    """
    Get the longest streak of habit.

    Args:
        habit(Habit): The habit from which the longest series should be calculated

    Returns:
        int: The value of the longest streak.

    Raises:
        TypeError: Habit not of type Habit.
        TypeError: Creation time not of type datetime.datetime.
        TypeError: Completed dates is not iterable.
    """
    #check if habit keywords are callable.
    try:
        creation_time=habit["creation_time"]
        frequency=habit["frequency"]
        completed_dates=habit["completed_dates"]
    except (KeyError,TypeError) as exc:
        raise TypeError("Habit not of type Habit.") from exc

    #initialise the streak and longest streak count
    streak, longest_streak = (0,0)

    #define today as the date from today
    today = date.today()
    try:
        #change creation_time of habit to date.
        creation_day = creation_time.date()
    except AttributeError as exc:
        raise TypeError("Creation time not of type datetime.datetime.") from exc

    #set today to the first day of the actuell period
    today = today - (today-creation_day)%timedelta(days=frequency)

    try:
        while today >= creation_day:
            if today in completed_dates:
                #count today to the streak
                streak += 1
            else:
                #start new streak
                streak = 0
            #set longes streak
            longest_streak = max(longest_streak,streak)
            #set today to one day before today
            today -= timedelta(days=frequency)
    except TypeError as exc:
        raise TypeError("Completed dates is not iterable.") from exc

    return longest_streak

def get_longest_streak_of_all(habit_list:list)->int:
    """
    Get the longest streak of all habits.

    Args:
        habit_list (list): The habits from which the longest series should be calculated

    Returns:
        int: The value of the longest streak of all habits.

    Raises:
        TypeError: Habit list is not a list.
    """
    if not isinstance(habit_list,list):
        raise TypeError("Habit list is not a list.")

    over_all_longest_streak = 0
    for habit in habit_list:
        try:
            longest_streak = get_longest_streak(habit=habit)
        except TypeError:
            continue
        over_all_longest_streak = max(over_all_longest_streak,longest_streak)
    return over_all_longest_streak

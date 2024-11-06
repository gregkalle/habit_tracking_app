"""
NAME
    analytics

DESCRIPTION
    Modul which contains the functions in functional programming paradigm for
    the habit tracking app.
"""
from datetime import date, timedelta
#from scr.habit import Habit


def get_current_tracked_habit(habit_id,habit_list):
    for habit in habit_list:
        if habit.habit_id == habit_id:
            return habit
        
def get_all_current_tracked_habits(habit_list, id_list):
    result = []
    for habit_id in id_list:
        result.append(get_current_tracked_habit(habit_id,habit_list))
    return result

def get_habit_with_frequency(habit_list, frequency):
    return [habit for habit in habit_list if habit.completion.frequency == frequency]

def get_current_streak(completed_dates, frequency, creation_time):
    """
    Calculate the actuell streak count.

    Returns:
        int: The number of consecutive periods the habit was fulfilled included today.
    """
    today = date.today()
    today = today - (today-creation_time.date())%timedelta(days=frequency)

    streak = 0
    while today in completed_dates:
        streak += 1
        today -= timedelta(days=frequency)
    return streak

def get_longest_streak(completed_dates, frequency, creation_time):
    streak, longest_streak = (0,0)
    today = date.today()
    today = today - (today-creation_time.date())%timedelta(days=frequency)

    while today >= creation_time.date():
        if today in completed_dates:
            streak += 1
        else:
            streak = 0
        longest_streak = max(longest_streak,streak)
        today -= timedelta(days=frequency)
    return longest_streak
    
def get_longest_streak_of_all(habit_list):
    streak_list = []
    try:
        for habit in habit_list:
            longest_streak = get_longest_streak(completed_dates=habit.completion.completed_dates,
                                                frequency=habit.completion.frequency,
                                                creation_time=habit.completion.creation_time)
            streak_list.append(longest_streak)
    except AttributeError as exc:
        raise AttributeError("no habit") from exc
    return max(streak_list)

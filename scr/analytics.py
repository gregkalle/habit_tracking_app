from scr.habit import Habit

class Analytics:
    """
    
    """

    MIN_DEFAULT_HABIT = 5

    def __init__(self):
        """
        load all habits
        """
        self.all_habits = Habit.load_all()

        # creates the missing amount of habits to the MIN_DEFAULT_HABIT value
        if len(self.all_habits) < Analytics.MIN_DEFAULT_HABIT:
            for i in range(Analytics.MIN_DEFAULT_HABIT - len(self.all_habits)):
                habit = Habit(name = f"Default habit name {i}", description=f"Default habit description {i}")
                habit.save()
                self.all_habits.append(habit)

    
    @classmethod
    def current_tracked_habit(cls, habit_list, habit_id):
        return [habit for habit in habit_list if habit.habit_id == habit_id][0]

    @classmethod
    def habit_with_frequency(cls, habit_list, frequency):
        return [habit for habit in habit_list if habit.completion.frequency == frequency]

    @classmethod
    def get_alll_longest_streaks(cls, habit_list):
        return {habit.habit_id : habit.completion.calculate_longest_streak() for habit in habit_list}
    
    @classmethod
    def get_longest_streak(cls, habit):
        return habit.completion.calculate_longest_streak()
    
    @classmethod
    def get_all_current_streaks(cls, habit_list):
        return {habit.habit_id : habit.completion.calculate_streak() for habit in habit_list}
    
    @classmethod
    def get_current_streak(cls, habit):
        return habit.completion.calculate_streak()
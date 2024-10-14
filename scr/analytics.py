from habit import Habit

class Analytics:
    """
    
    """

    def __init__(self):
        """
        load all habits
        """
        self.all_habits = Habit.load_all()
    
    @classmethod
    def current_tracked_habit(cls, habit_list, habit_id):
        pass

    @classmethod
    def habit_with_frequency(cls, habit_list, frequency):
        pass

    @classmethod
    def get_longest_streaks(cls, habit_list):
        pass
    
    @classmethod
    def most_struggled_habit(cls, habit_list):
        pass
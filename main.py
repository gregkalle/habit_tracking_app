from scr.analytics import Analytics
from scr.habit import Habit
from scr.completion import Completion

#Habit.delete(1)

#habit = Habit()
habit = Habit.load_all()[0]

habit.completion.mark_completed()

habit.save()

habit1 = Habit.load(habit.habit_id)

help(Completion)



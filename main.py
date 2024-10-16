from scr.analytics import Analytics
from scr.habit import Habit


habit = Habit()

habit.save()

habit1 = Habit.load_all()

print(type(habit))

print(isinstance(habit,type(Habit())))

print(len(habit1))

print(habit1[0].completion.creation_time)

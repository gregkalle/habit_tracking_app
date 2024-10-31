from datetime import datetime, timedelta
from scr.habit import Habit

storage = Habit.DEFAULT_STORAGE_STRATEGY

creation_time = datetime(year=2024,month=9,day=30,hour=8)

habit_data=[]
walk=[]
for i in range(28):
    walk.append(creation_time.date() + i* timedelta(days=1))
clean=[]
for i in range(7,21):
    clean.append(creation_time.date() + i* timedelta(days=1))
push_up=[]
for i in range(7,21):
    push_up.append(creation_time.date() + i* timedelta(days=1))
apple=[]
for i in range(14):
    apple.append(creation_time.date() + i* timedelta(days=1))
for i in range(21,28):
    apple.append(creation_time.date() + i* timedelta(days=1))
swim=[]
for i in range(7):
    swim.append(creation_time.date() + i* timedelta(days=1))
for i in range(21,28):
    swim.append(creation_time.date() + i* timedelta(days=1))
habit_data.append({"name": "Go for a walk", "description": "Walking at least 1km a day.",
         "frequency": 1, "completed_dates": walk,
         "creation_time": creation_time,})
habit_data.append({"name": "Clean the house", "description": "Clean the house once a week.",
         "frequency": 7, "completed_dates": clean,
         "creation_time": creation_time,})
habit_data.append({"name": "Push ups", "description": "Excercise 10 push-ups every day.",
         "frequency": 1, "completed_dates": push_up,
         "creation_time": creation_time,})
habit_data.append({"name": "Eat an apple", "description": "An apple a day keeps the doctor away.",
         "frequency": 1, "completed_dates": apple,
         "creation_time": creation_time,})
habit_data.append({"name": "Swimming", "description": "Swim 1km in the local swimming pool.",
         "frequency": 7, "completed_dates": swim,
         "creation_time": creation_time,})
for data in habit_data:
    habit = Habit(name=data["name"], description=data["description"],frequency=data["frequency"],
                completed_dates=data["completed_dates"],creation_time=data["creation_time"])
    habit.save()

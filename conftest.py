import os
from datetime import datetime, timedelta
import pytest
from freezegun import freeze_time
from scr.habit import Habit
from scr.sqlite_storage import SQLiteStorage

@pytest.fixture(scope="session", autouse=True)
def set_up():
    
    #remove test database if exists.
    if os.path.exists("test/test_data.db"):
        os.remove("test/test_data.db")

    #Set database
    Habit.DEFAULT_STORAGE_STRATEGY = SQLiteStorage(data_base="test/test_data.db")

    #create habit data
    habit_data = create_habit_data()

    #create habit and save into database
    for data in habit_data:
        habit = Habit(name=data["name"], description=data["description"],frequency=data["frequency"],
                completed_dates=data["completed_dates"],creation_time=data["creation_time"])
        habit.save()
    
    yield

    #remove test database
    if os.path.exists("test/test_data.db"):
        os.remove("test/test_data.db")



@pytest.fixture
@freeze_time("2024-09-30")
def create_habits():
    """
    Creates habits with which the habit tracker app is tested.
    """
    test_habit1=Habit(name="Go for a walk",description="Walking at least 1km a day.",habit_id=1,frequency=1,)
    test_habit2=Habit(name="Clean the house", description="Clean the house once a week.",habit_id=2,frequency=7)
    test_habit3=Habit(name="Push ups", description="Excercise 10 push-ups every day.",habit_id=3,frequency=1)
    test_habit4=Habit(name="Eat an apple", description="An apple a day keeps the doctor away.",habit_id=4,frequency=1)
    test_habit5=Habit(name="Swimming", description="Swim 1km in the local swimming pool.",habit_id=5,frequency=7)
    return [test_habit1,test_habit2,test_habit3,test_habit4,test_habit5]


@pytest.fixture
def data_base_path():
    return "test/test_data.db"


def create_habit_data():
    """
    Creats the habit_data which is stored in the test database.
    """
    creation_time = datetime(year=2024,month=9,day=30)
    habit_data=[]

    #set completed dates
    walk=[]
    for i in range(28):
        walk.append(creation_time.date() + i* timedelta(days=1))
    clean=[]
    for i in [7,14]:
        clean.append(creation_time.date() + i* timedelta(days=1))
    push_up=[]
    for i in range(7,21):
        push_up.append(creation_time.date() + i* timedelta(days=1))
    apple=[]
    apple_dates = list(range(14))+list(range(21,28))
    for i in apple_dates:
        apple.append(creation_time.date() + i* timedelta(days=1))
    swim=[]
    for i in [0,21]:
        swim.append(creation_time.date() + i* timedelta(days=1))
    
    #set the habit data.
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
    return habit_data
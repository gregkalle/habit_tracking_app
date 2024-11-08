import pytest
from freezegun import freeze_time
from scr.habit import Habit


@pytest.fixture
@freeze_time("2024-09-30")
def create_habits():
    test_habit1=Habit(name="Go for a walk",description="Walking at least 1km a day.",habit_id=1,frequency=1,)
    test_habit2=Habit(name="Clean the house", description="Clean the house once a week.",habit_id=2,frequency=7)
    test_habit3=Habit(name="Push ups", description="Excercise 10 push-ups every day.",habit_id=3,frequency=1)
    test_habit4=Habit(name="Eat an apple", description="An apple a day keeps the doctor away.",habit_id=4,frequency=1)
    test_habit5=Habit(name="Swimming", description="Swim 1km in the local swimming pool.",habit_id=5,frequency=7)
    return [test_habit1,test_habit2,test_habit3,test_habit4,test_habit5]
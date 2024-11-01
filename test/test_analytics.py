import pytest
from scr.analytics import Analytics
from scr.habit import Habit
from scr.sqlite_storage import SQLiteStorage

#set database to test database
Habit.DEFAULT_STORAGE_STRATEGY = SQLiteStorage("test/test_data.db")

test_habit1=Habit(name="Go for a walk",description="Walking at least 1km a day.",habit_id=1)
test_habit2=Habit(name="Clean the house", description="Clean the house once a week.",habit_id=2)
test_habit3=Habit(name="Push ups", description="Excercise 10 push-ups every day.",habit_id=3)
test_habit4=Habit(name="Eat an apple", description="An apple a day keeps the doctor away.",habit_id=4)
test_habit5=Habit(name="Swimming", description="Swim 1km in the local swimming pool.",habit_id=5)
habit_list=[test_habit1,test_habit2,test_habit3,test_habit4,test_habit5]


@pytest.mark.parametrize("habit",habit_list)
def test_load_habits(habit):
    habits = Analytics.load_habits()
    assert habit in habits

@pytest.mark.parametrize("habit",[habit_list])
def test_get_habit_ids(habit):
    id_list = Analytics.get_habit_ids(habit_list=habit)
    for j,habit_id in enumerate(id_list):
        assert j+1== habit_id

@pytest.mark.parametrize("habit",habit_list[0:2])
def test_create_new_habit(habit):
    habit1 = Analytics.create_new_habit(habit_name="Go for a walk",habit_description="Walking at least 1km a day.",frequency=7)
    habit2 = Analytics.create_new_habit(habit_name="Clean the house",habit_description="Clean the house once a week.",frequency=1)
    assert habit1 == habit and habit1.completion.frequency == 7
    assert habit2 == habit and habit2.completion.frequency == 1
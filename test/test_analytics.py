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

@pytest.mark.parametrize("habit, habit_id",[(habit,habit_list.index(habit)+1) for habit in habit_list])
def test_get_current_tracked_habit(habit,habit_id):
    currend_tracked_habit = Analytics.get_current_tracked_habit(habit_id=habit_id)
    assert currend_tracked_habit == habit

def test_get_current_tracked_habit_error_masseges():
    missing_id = 0
    with pytest.raises(ValueError,match=f"There is no habit with id {missing_id} in the database."):
        Analytics.get_current_tracked_habit(missing_id)

@pytest.mark.parametrize("habit",[habit_list])
def test_get_habit_ids(habit):
    id_list = Analytics.get_habit_ids(habit_list=habit)
    for j,habit_id in enumerate(id_list):
        assert j+1== habit_id

@pytest.mark.parametrize("habit",[habit_list[0:2]])
def test_create_new_habit(habit):
    habit1 = Analytics.create_new_habit(habit_name="Go for a walk",habit_description="Walking at least 1km a day.",frequency=7)
    habit2 = Analytics.create_new_habit(habit_name="Clean the house",habit_description="Clean the house once a week.",frequency=1)
    habit1.habit_id = 1
    habit2.habit_id = 2
    assert habit1 == habit[0] and habit1.completion.frequency == 7
    assert habit2 == habit[1] and habit2.completion.frequency == 1

def test_create_new_habit_error_messages():
    with pytest.raises(TypeError, match="Habit name must be string."):
        Analytics.create_new_habit(habit_name=None,habit_description="Walking at least 1km a day.",frequency=7)
    with pytest.raises(TypeError, match="Habit description must be string."):
        Analytics.create_new_habit(habit_name="Go for a walk",habit_description=None,frequency=7)
    with pytest.raises(TypeError, match="Frequency must be integer."):
        Analytics.create_new_habit(habit_name="Go for a walk",habit_description="Walking at least 1km a day.",frequency=None)
    with pytest.raises(ValueError, match="Frequency must be greater than 0."):
        Analytics.create_new_habit(habit_name="Go for a walk",habit_description="Walking at least 1km a day.",frequency=0)


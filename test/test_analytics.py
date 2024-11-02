import pytest
from scr.analytics import Analytics
from scr.habit import Habit
from scr.sqlite_storage import SQLiteStorage

#set database to test database
Habit.DEFAULT_STORAGE_STRATEGY = SQLiteStorage("test/test_data.db")

test_habit1=Habit(name="Go for a walk",description="Walking at least 1km a day.",habit_id=1,frequency=1)
test_habit2=Habit(name="Clean the house", description="Clean the house once a week.",habit_id=2,frequency=7)
test_habit3=Habit(name="Push ups", description="Excercise 10 push-ups every day.",habit_id=3,frequency=1)
test_habit4=Habit(name="Eat an apple", description="An apple a day keeps the doctor away.",habit_id=4,frequency=1)
test_habit5=Habit(name="Swimming", description="Swim 1km in the local swimming pool.",habit_id=5,frequency=7)
test_habit_list=[test_habit1,test_habit2,test_habit3,test_habit4,test_habit5]


@pytest.mark.parametrize("habit",test_habit_list)
def test_load_habits(habit):
    habits = Analytics.load_habits()
    assert habit in habits
    assert len(habits) == 5

@pytest.mark.parametrize("habit, habit_id",[(habit,test_habit_list.index(habit)+1) for habit in test_habit_list])
def test_get_current_tracked_habit(habit,habit_id):
    currend_tracked_habit = Analytics.get_current_tracked_habit(habit_id=habit_id)
    assert currend_tracked_habit == habit

def test_get_current_tracked_habit_errors():
    missing_id = 0
    with pytest.raises(ValueError,match=f"There is no habit with id {missing_id} in the database."):
        Analytics.get_current_tracked_habit(missing_id)

@pytest.mark.parametrize("habit_list,frequency",[(test_habit_list,1),(test_habit_list,7)])
def test_get_habits_with_frequency(habit_list,frequency):
    habits=Analytics.get_habits_with_frequency(habit_list=habit_list,frequency=frequency)
    for habit in habits:
        assert habit.completion.frequency == frequency

@pytest.mark.parametrize("habit_list,frequency",[(test_habit_list,7)])
def test_get_habit_with_frequency_errors(habit_list,frequency):
    with pytest.raises(TypeError,match="Frequency not of type integer."):
        Analytics.get_habits_with_frequency(habit_list=habit_list,frequency="seven")
    with pytest.raises(TypeError,match="Object not of type Habit."):
        Analytics.get_habits_with_frequency(habit_list=[Habit(name=None,description=None),"Not a habit object."],frequency=frequency)

@pytest.mark.parametrize("habit_id,result",[(1,28),(2,2),(3,14),(4,14),(5,1)])
def test_get_longest_streak(habit_id,result):
    habit = Analytics.get_current_tracked_habit(habit_id=habit_id)
    assert Analytics.get_longest_streak(habit=habit) == result

def test_get_longest_streak_errors():
    with pytest.raises(TypeError,match="Object not of type Habit."):
        Analytics.get_longest_streak("No habit object.")



@pytest.mark.parametrize("habit_list",[test_habit_list])
def test_get_habit_ids(habit_list):
    id_list = Analytics.get_habit_ids(habit_list=habit_list)
    for j,habit_id in enumerate(id_list):
        assert j+1== habit_id

@pytest.mark.parametrize("habit",[test_habit_list[0:2]])
def test_create_new_habit(habit):
    habit1 = Analytics.create_new_habit(habit_name="Go for a walk",habit_description="Walking at least 1km a day.",frequency=7)
    habit2 = Analytics.create_new_habit(habit_name="Clean the house",habit_description="Clean the house once a week.",frequency=1)
    habit1.habit_id = 1
    habit2.habit_id = 2
    assert habit1 == habit[0] and habit1.completion.frequency == 7
    assert habit2 == habit[1] and habit2.completion.frequency == 1

def test_create_new_habit_errors():
    with pytest.raises(TypeError, match="Habit name must be string."):
        Analytics.create_new_habit(habit_name=None,habit_description="Walking at least 1km a day.",frequency=7)
    with pytest.raises(TypeError, match="Habit description must be string."):
        Analytics.create_new_habit(habit_name="Go for a walk",habit_description=None,frequency=7)
    with pytest.raises(TypeError, match="Frequency must be integer."):
        Analytics.create_new_habit(habit_name="Go for a walk",habit_description="Walking at least 1km a day.",frequency=None)
    with pytest.raises(ValueError, match="Frequency must be greater than 0."):
        Analytics.create_new_habit(habit_name="Go for a walk",habit_description="Walking at least 1km a day.",frequency=0)


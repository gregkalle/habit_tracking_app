import pytest
from freezegun import freeze_time
import scr.analytics as ana
from scr.habit import Habit


@pytest.fixture
def create_habits():
    test_habit1=Habit(name="Go for a walk",description="Walking at least 1km a day.",habit_id=1,frequency=1)
    test_habit2=Habit(name="Clean the house", description="Clean the house once a week.",habit_id=2,frequency=7)
    test_habit3=Habit(name="Push ups", description="Excercise 10 push-ups every day.",habit_id=3,frequency=1)
    test_habit4=Habit(name="Eat an apple", description="An apple a day keeps the doctor away.",habit_id=4,frequency=1)
    test_habit5=Habit(name="Swimming", description="Swim 1km in the local swimming pool.",habit_id=5,frequency=7)
    return [test_habit1,test_habit2,test_habit3,test_habit4,test_habit5]
        

@pytest.mark.parametrize("habit_id",[1,2,3,4,5])
def test_get_current_tracked_habit(create_habits,habit_id):
    currend_tracked_habit = ana.get_current_tracked_habit(habit_id=habit_id,habit_list=create_habits)
    assert currend_tracked_habit == create_habits[habit_id-1]

def test_get_current_tracked_habit_errors(create_habits):
    missing_id = 0
    with pytest.raises(ValueError,match=f"There is no habit with id {missing_id} in the list."):
        ana.get_current_tracked_habit(habit_id=missing_id,habit_list=create_habits)

@pytest.mark.parametrize("id_list",[[1,2,3],[],[4,5]])
def test_get_all_current_tracked_habits(create_habits,id_list):
    all_tracked_habits = ana.get_all_current_tracked_habits(id_list=id_list,habit_list=create_habits)
    assert len(all_tracked_habits) == len(id_list)
    for habit in all_tracked_habits:
        assert habit in [element for element in create_habits if element["habit_id"] in id_list]

def test_get_all_current_tracked_habits_errors(create_habits):
    missing_id = [1,2,0,3]
    with pytest.raises(ValueError,match=f"There is no habit with id {missing_id[2]} in the habit list."):
        ana.get_all_current_tracked_habits(id_list=missing_id,habit_list=create_habits)

@pytest.mark.parametrize("frequency",[1,7])
def test_get_habits_with_frequency(create_habits, frequency):
    habits_with_frequency=ana.get_habit_with_frequency(habit_list=create_habits,frequency=frequency)
    for habit in habits_with_frequency:
        assert habit["frequency"] == frequency
    #test if all habits with frequency is in habits with frequency.
    habits_without_frequency = [habit for habit in create_habits if habit["frequency"]!=frequency]
    assert len(habits_without_frequency) == len(create_habits) - len(habits_with_frequency)

def test_get_habit_with_frequency_errors():
    with pytest.raises(TypeError,match="Object not of type Habit."):
        ana.get_habit_with_frequency(habit_list=["Not a habit object."],frequency=7)
        ana.get_habit_with_frequency(habit_list=object(),frequency=7)

@freeze_time("2024-10-27")
@pytest.mark.parametrize("position,result",[(0,28),(1,0),(2,0),(3,7),(4,1)])
def test_get_current_streak(position,result):
    habit_list = Habit.load_all()
    assert ana.get_current_streak(habit=habit_list[position]) == result

def test_get_current_streak_errors():
    fake_habit ={"frequency": 1, "creation_time":"No datetime object.", "completed_dates":[]}
    with pytest.raises(TypeError,match="Creation time not of type datetime.datetime."):
        ana.get_current_streak(habit=fake_habit)

@pytest.mark.parametrize("position,result",[(0,28),(1,2),(2,14),(3,14),(4,1)])
def test_get_longest_streak(position,result):
    habit_list = Habit.load_all()
    assert ana.get_longest_streak(habit=habit_list[position]) == result

def test_get_longest_streak_errors():
    fake_habit ={"frequency": 1, "creation_time":"No datetime object.", "completed_dates":[]}
    with pytest.raises(TypeError,match="Creation time not of type datetime.datetime."):
        ana.get_longest_streak(habit=fake_habit)

@pytest.mark.parametrize("result",[28])
def test_def_get_longest_streak_of_all(result):
    habit_list = Habit.load_all()
    assert ana.get_longest_streak_of_all(habit_list=habit_list) == result

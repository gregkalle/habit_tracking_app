from datetime import date
import pytest
from freezegun import freeze_time
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


@pytest.mark.parametrize("habit_list",[test_habit_list])
def test_load_habits(habit_list):
    habits = Analytics.load_habits()
    assert len(habits) == len(habit_list)
    for habit in habits:
        assert habit in habit_list
    

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
    habits_with_frequency=Analytics.get_habits_with_frequency(habit_list=habit_list,frequency=frequency)
    for habit in habits_with_frequency:
        assert habit.completion.frequency == frequency
    #test if all habits with frequency is in habits with frequency.
    habits_without_frequency = [habit for habit in habit_list if habit.completion.frequency!=frequency]
    assert len(habits_without_frequency) == len(habit_list) - len(habits_with_frequency)

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

@freeze_time("2024-10-27")
@pytest.mark.parametrize("habit_id,result",[(1,28),(2,0),(3,0),(4,7),(5,1)])
def test_get_current_streak(habit_id,result):
    habit = Analytics.get_current_tracked_habit(habit_id=habit_id)
    assert Analytics.get_current_streak(habit=habit) == result

def test_get_current_streak_errors():
    with pytest.raises(TypeError,match="Object not of type Habit."):
        Analytics.get_current_streak("No habit object.")

@freeze_time("2024-10-27")
def test_habit_to_dict():
    key_list=["selected", "habit name", "description", "frequency","current streak", "longest streak"]
    value_list=[4,"Eat an apple","An apple a day keeps the doctor away.",1,7,14]
    habit_dictionary = Analytics.habit_to_dict(Analytics.get_current_tracked_habit(4))
    for i,name in enumerate(habit_dictionary.keys()):
        assert name == key_list[i]
        assert habit_dictionary[name] == value_list[i]

def test_habit_to_dict_errors():
    with pytest.raises(TypeError,match="Object not of type Habit."):
        Analytics.habit_to_dict("No habit object.")

def test_habit_to_dict_error():
    with pytest.raises(TypeError,match="Object not of type Habit."):
        Analytics.habit_to_dict("No habit object.")


@pytest.mark.parametrize("habit_list",[test_habit_list])
def test_get_habit_ids(habit_list):
    id_list = Analytics.get_habit_ids(habit_list=habit_list)
    for j,habit_id in enumerate(id_list):
        assert j+1== habit_id

def test_get_habit_ids_error():
    with pytest.raises(TypeError,match="Object not of type Habit."):
        Analytics.get_habit_ids([Habit(name=None,description=None),"No habit object."])

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

@pytest.mark.parametrize("habit_id, habit",[(1,test_habit1),(2,test_habit2),(3,test_habit3)])
def test_change_habit_name_description(habit_id,habit):
    changed_habit = Analytics.change_habit_name_description(habit_id=habit_id,habit_name="New habit name.")
    assert changed_habit.name == "New habit name."
    changed_habit = Analytics.change_habit_name_description(habit_id=habit_id,habit_description="new description")
    assert changed_habit.description == "new description"
    changed_habit = Analytics.change_habit_name_description(habit_id=habit_id,habit_name="new name", habit_description="new description")
    assert changed_habit.name == "new name" and changed_habit.description == "new description"
    changed_habit = Analytics.change_habit_name_description(habit_id=habit_id)
    assert changed_habit == habit

def test_change_habit_name_description_errors():
    missing_id = 0
    with pytest.raises(ValueError, match=f"There is no habit with id {missing_id} in the database."):
        Analytics.change_habit_name_description(habit_id=missing_id)

@pytest.mark.order(-1)
def test_delete_habit():
    #neuen habit erschaffen und in db speichern, dann löschen und dann fehlermeldung checken von analytics.get_currend_tracked_habit
    deletable_habit = Habit(name=None,description=None)
    deletable_habit.save()
    delete_id = deletable_habit.habit_id
    assert deletable_habit == Analytics.get_current_tracked_habit(habit_id=delete_id)
    Analytics.delete_habit(habit_id=delete_id)
    with pytest.raises(ValueError):
        Analytics.get_current_tracked_habit(delete_id)

def test_delete_habit_errors():
    delete_id = 7
    with pytest.raises(ValueError,match=f"There is no habit with id {delete_id} in the database."):
        Analytics.delete_habit(delete_id)

@pytest.mark.parametrize("habit_id, insert_date, marked_date",
                        [(1,date(day=31,month=10,year=2024),date(day=31,month=10,year=2024)),
                         (2,date(day=31,month=10,year=2024),date(day=28,month=10,year=2024))])
def test_get_marked_completed(habit_id, insert_date, marked_date):
    habit = Analytics.get_marked_completed(habit_id=habit_id,date=insert_date)
    assert marked_date in habit.completion.completed_dates

def test_get_marked_completed_error():
    habit_id = 7
    with pytest.raises(ValueError,match=f"There is no habit with id {habit_id} in the database."):
        Analytics.get_marked_completed(habit_id=habit_id)

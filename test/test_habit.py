import pytest
from scr.habit import Habit

@pytest.fixture
def create_habits():
    test_habit1=Habit(name="Go for a walk",description="Walking at least 1km a day.",habit_id=1,frequency=1)
    test_habit2=Habit(name="Clean the house", description="Clean the house once a week.",habit_id=2,frequency=7)
    test_habit3=Habit(name="Push ups", description="Excercise 10 push-ups every day.",habit_id=3,frequency=1)
    test_habit4=Habit(name="Eat an apple", description="An apple a day keeps the doctor away.",habit_id=4,frequency=1)
    test_habit5=Habit(name="Swimming", description="Swim 1km in the local swimming pool.",habit_id=5,frequency=7)
    return [test_habit1,test_habit2,test_habit3,test_habit4,test_habit5]

def test__eq__():
    assert Habit(name="habit 1",description="habit 1") == Habit(name="habit 1",description="habit 1")
    assert Habit(name="habit 2",description="habit 2",habit_id=1) == Habit(name="habit 2",description="habit 2",habit_id=1)
    assert Habit(name="habit 1",description="habit 2",habit_id=1) != Habit(name="habit 2",description="habit 2",habit_id=1)
    assert Habit(name="habit 2",description="habit 1",habit_id=1) != Habit(name="habit 2",description="habit 2",habit_id=1)
    assert Habit(name="habit 2",description="habit 2",habit_id=2) != Habit(name="habit 2",description="habit 2",habit_id=1)


@pytest.mark.parametrize("habit_id",[[1,2,3,4,5]])
def test_load(create_habits, habit_id):
    for i,habit in enumerate(create_habits):
        assert habit == Habit.load(habit_id=habit_id[i])

def test_load_all(create_habits):
    habits = Habit.load_all()
    assert len(habits) == len(create_habits)
    for habit in habits:
        assert habit in create_habits

@pytest.mark.order(-2)
def test_save_and_delete():
    habit = Habit(name=None,description=None)
    habit.save()
    assert habit == Habit.load(habit_id=habit.habit_id)
    Habit.delete(habit_id=habit.habit_id)
    assert not Habit.load(habit_id=habit.habit_id)

def test_save_errors():
    not_savable_habit = Habit(name=object(),description=object())
    with pytest.raises(TypeError,match="Habit is not savable."):
        not_savable_habit.save()

def test_delete_error():
    delete_id = 7
    with pytest.raises(ValueError,match="ID is not in database."):
        Habit.delete(delete_id)

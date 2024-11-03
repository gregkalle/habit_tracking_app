import pytest
from scr.habit import Habit

def test__eq__():
    assert Habit(name="habit 1",description="habit 1") == Habit(name="habit 1",description="habit 1")
    assert Habit(name="habit 2",description="habit 2",habit_id=1) == Habit(name="habit 2",description="habit 2",habit_id=1)
    assert Habit(name="habit 1",description="habit 2",habit_id=1) != Habit(name="habit 2",description="habit 2",habit_id=1)
    assert Habit(name="habit 2",description="habit 1",habit_id=1) != Habit(name="habit 2",description="habit 2",habit_id=1)
    assert Habit(name="habit 2",description="habit 2",habit_id=2) != Habit(name="habit 2",description="habit 2",habit_id=1)

def test_save():
    pass

def test_load():
    pass

def test_load_all():
    pass

def test_delete():
    pass
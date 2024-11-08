from datetime import date, datetime
import pytest
from freezegun import freeze_time
from scr.habit import Habit
from scr.sqlite_storage import SQLiteStorage


class TestHabits:

    def setup_method(self):
        #set database to test database
        Habit.DEFAULT_STORAGE_STRATEGY = SQLiteStorage("test/test_data.db")

    def test__eq__(self):
        assert Habit(name="habit 1",description="habit 1") == Habit(name="habit 1",description="habit 1")
        assert Habit(name="habit 2",description="habit 2",habit_id=1) == Habit(name="habit 2",description="habit 2",habit_id=1)
        assert Habit(name="habit 1",description="habit 2",habit_id=1) != Habit(name="habit 2",description="habit 2",habit_id=1)
        assert Habit(name="habit 2",description="habit 1",habit_id=1) != Habit(name="habit 2",description="habit 2",habit_id=1)
        assert Habit(name="habit 2",description="habit 2",habit_id=2) != Habit(name="habit 2",description="habit 2",habit_id=1)

    @pytest.mark.parametrize("prop,value",[("name","Go for a walk"),("description","Walking at least 1km a day."),
                                               ("habit_id",1),("frequency",1),("creation_time",datetime(year=2024,day=30,month=9)),
                                               ("completed_dates",[])])
    def test__getitem__(self,create_habits,prop,value):
        habit = create_habits[0]
        assert habit[prop] == value

    def test__setitem__(self):
        habit = Habit(name="name",description="description")
        habit["name"] = "new name"
        habit["description"] = "new description"
        assert habit["name"] == "new name"
        assert habit["description"] == "new description"

    @pytest.mark.parametrize("habit_id",[[1,2,3,4,5]])
    def test_load(self, create_habits, habit_id):
        for i,habit in enumerate(create_habits):
            assert habit == Habit.load(habit_id=habit_id[i])

    def test_load_all(self,create_habits):
        habits = Habit.load_all()
        assert len(habits) == len(create_habits)
        for habit in habits:
            assert habit in create_habits

    @pytest.mark.order(-2)
    def test_save_and_delete(self):
        habit = Habit(name=None,description=None)
        habit.save()
        assert habit == Habit.load(habit_id=habit["habit_id"])
        Habit.delete(habit_id=habit["habit_id"])
        assert not Habit.load(habit_id=habit["habit_id"])

    def test_save_errors(self):
        not_savable_habit = Habit(name=object(),description=object())
        with pytest.raises(TypeError,match="Habit is not savable."):
            not_savable_habit.save()

    def test_delete_error(self):
        delete_id = 7
        with pytest.raises(ValueError,match="ID is not in database."):
            Habit.delete(delete_id)

    @pytest.mark.parametrize("habit_id,name,description,result",[(1,"new name","new description",("new name","new description")),
                                                          (1,"new name",None,("new name","Walking at least 1km a day.")),
                                                          (1,None,"new description",("Go for a walk","new description")),
                                                          (1,None,None,("Go for a walk","Walking at least 1km a day."))])
    def test_change_habit_name_description(self,habit_id,name,description,result):
        habit = Habit.change_habit_name_description(habit_id=habit_id,habit_name=name,habit_description=description)
        assert habit["name"] == result[0]
        assert habit["description"] == result[1]

    def test_change_habit_name_description_error(self):
        missing_id = 0
        with pytest.raises(ValueError,match=f"There is no habit with id {missing_id} in the database."):
            Habit.change_habit_name_description(habit_id=missing_id)

    @freeze_time("2024-10-27")
    @pytest.mark.parametrize("habit_data",[[1,"Go for a walk","Walking at least 1km a day.",
                                            1,28,28]])
    def test_habit_data(self,habit_data):
        habit = Habit.load(habit_id=habit_data[0])
        data = Habit.habit_data(habit=habit)
        for i,value in enumerate(data):
            assert value == habit_data[i]

    def test_habit_data_error(self):
        with pytest.raises(TypeError,match="Object not of type Habit."):
            Habit.habit_data(habit="No habit object.")

    @pytest.mark.order(-1)
    def test_save_with_marked_date(self):
        habit = Habit(name="name",description="description",frequency=1)
        habit.save()
        habit.completion.mark_completed(date.today())
        habit.save()
        habit = Habit.load(habit_id=habit["habit_id"])
        assert habit["completed_dates"][0] == date.today()
        habit.completion.mark_completed(date.today())
        habit.save()
        habit = Habit.load(habit_id=habit["habit_id"])
        assert len(habit["completed_dates"]) == 1
        habit.delete(habit_id=habit["habit_id"])

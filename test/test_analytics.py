import pytest
from scr.analytics import Analytics
from scr.habit import Habit
from scr.sqlite_storage import SQLiteStorage

test_habit1 = Habit(name="Go for a walk",description="Walking at least 1km a day.",habit_id=1)
test_habit5 = Habit(name="Swimming",description="Swim 1km in the local swimming pool.",habit_id=5)

@pytest.fixture
def set_habit_db(request):
    #set database to test_data.db
    Habit.DEFAULT_STORAGE_STRATEGY = SQLiteStorage("test/test_data.db")
    print(request.param)
    return request.param

@pytest.mark.parametrize("set_habit_db",[test_habit1,test_habit5],indirect=True)
def test_load_habits(request):
    habits = Analytics.load_habits
    for test_habit in request:
        assert any(list(map(lambda x,y: x == y, habits,[test_habit])))

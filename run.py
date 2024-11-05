from freezegun import freeze_time
from main import main
from scr.habit import Habit
from scr.sqlite_storage import SQLiteStorage

Habit.DEFAULT_STORAGE_STRATEGY = SQLiteStorage("test/test_data.db")

@freeze_time("2024-10-27")
def run():
    main()

run()

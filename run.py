from freezegun import freeze_time
from scr.main import main

@freeze_time("2024-10-27")
def run():
    main()

run()

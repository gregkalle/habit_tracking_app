from datetime import date, datetime, timedelta
import pytest
from freezegun import freeze_time
from scr.completion import Completion

def test_completion_error():
    with pytest.raises(ValueError,match="Frequency must be a positiv integer."):
        Completion(frequency=-1)

@freeze_time("2024-10-28")
@pytest.mark.parametrize("checked_date,added_date,completed_dates,frequency,length",
            [(None,date(day=28,month=10,year=2024),[date(day=21,month=10,year=2024)],1,2),
            (None,date(day=28,month=10,year=2024),[date(day=21,month=10,year=2024)],7,2),
            (date(day=14,month=10,year=2024),date(day=14,month=10,year=2024),[date(day=21,month=10,year=2024)],1,2),
            (date(day=14,month=10,year=2024),date(day=14,month=10,year=2024),[date(day=21,month=10,year=2024)],7,2),
            (date(day=21,month=10,year=2024),date(day=21,month=10,year=2024),[date(day=21,month=10,year=2024)],1,1),
            (date(day=22,month=10,year=2024),date(day=21,month=10,year=2024),[date(day=21,month=10,year=2024)],7,1),])
def test_mark_completed(checked_date,added_date,completed_dates,frequency,length):
    completion = Completion(frequency=frequency,completed_dates=completed_dates)
    completion.mark_completed(checked_date=checked_date)
    assert len(completion.completed_dates)==length
    assert added_date in completion.completed_dates

@pytest.fixture()
def create_completion(create_completion_arg):
    #create_completion_arg[0]=frequency
    #create_completion_arg[1]=periods
    creation_time = datetime(day=30,month=9,year=2024)
    completed_dates_1 = [creation_time.date() + i* timedelta(days=create_completion_arg[0]) for i in range(create_completion_arg[1])]
    completed_dates_2 = [creation_time.date() + 21*timedelta(days=1)+i* timedelta(days=create_completion_arg[0]) for i in range(int(create_completion_arg[1]/2))]
    completed_dates_3 = completed_dates_1 + completed_dates_2
    return [Completion(creation_time=creation_time,frequency=create_completion_arg[0],completed_dates=dates) for
                        dates in [completed_dates_1,completed_dates_2,completed_dates_3]]

@freeze_time("2024-10-27")
@pytest.mark.parametrize("create_completion_arg,results",[((1,14),(0,7,7)),((7,2),(0,1,1))])
def test_calculate_streak(create_completion, results):
    for i,completion in enumerate(create_completion):
        assert completion.calculate_streak() == results[i]

@pytest.mark.parametrize("create_completion_arg,results",[((1,14),(14,7,14)),((7,2),(2,1,2))])
def test_calculate_longest_streak(create_completion, results):
    for i,completion in enumerate(create_completion):
        assert completion.calculate_longest_streak() == results[i]

def test_validate_date():
    assert Completion.validate_date(date.today()) is None
    with pytest.raises(TypeError,match="The data must be of type datetime.date."):
        Completion.validate_date(datetime.today())
        Completion.validate_date(object())

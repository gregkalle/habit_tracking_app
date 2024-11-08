from datetime import date, datetime,timedelta
import pytest
from freezegun import freeze_time
from scr.completion import Completion

def test_completion_error():
    with pytest.raises(ValueError,match="Frequency must be a positiv integer."):
        Completion(frequency=-1)
    with pytest.raises(TypeError,match="Creation time must be of type datetime.datetime."):
        Completion(creation_time=date.today())
    with pytest.raises(TypeError,match="The elements of completed dates must be of type datetime.date."):
        Completion(completed_dates=datetime.now())
        Completion(completed_dates="Not type date")

@pytest.mark.parametrize("frequency,creation_time,completed_dates",[(1,datetime.now(),[date.today()])])
def test__getitem__(frequency,creation_time,completed_dates):
    completion = Completion(frequency=frequency,creation_time=creation_time,completed_dates=completed_dates)
    assert completion["frequency"] == 1
    assert completion["creation_time"]-creation_time == timedelta()
    assert completion["completed_dates"][0] - date.today() == timedelta()
    with pytest.raises(KeyError):
        completion["Not an item."]

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
    assert len(completion.record["completed_dates"])==length
    assert added_date in completion.record["completed_dates"]

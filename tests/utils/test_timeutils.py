import datetime as dt
import pytest
from dtctl.utils.timeutils import determine_date_range, fmttime, prstime, current_date, days_to_timedelta


def test_determine_date_range():
    # Somewhat of an integration test
    end_date, start_date = determine_date_range(5, None, None)
    assert end_date == current_date() + dt.timedelta(hours=23, minutes=59, seconds=59)
    assert start_date == current_date() - days_to_timedelta(5)

    end_date, start_date = determine_date_range(0, None, None)
    assert end_date == current_date() + dt.timedelta(hours=23, minutes=59, seconds=59)
    assert start_date == current_date() - days_to_timedelta(0)

    start_date_dt = current_date() - dt.timedelta(days=5, hours=23, minutes=59, seconds=59)
    end_date, start_date = determine_date_range(None, None, start_date_dt)
    assert end_date == current_date() + dt.timedelta(hours=23, minutes=59, seconds=59)
    assert start_date == start_date_dt

    with pytest.raises(TypeError) as exc_info:
        end_date, start_date = determine_date_range(None, None, None)

    assert isinstance(exc_info.value, TypeError)


def test_fmttime():
    timestamp_int = 1559290405
    time_to_fmt = current_date()
    timestamp_current_time = current_date().timestamp() * 1000

    assert timestamp_int == fmttime(timestamp_int)
    assert isinstance(fmttime(timestamp_int), int)
    assert timestamp_current_time == fmttime(time_to_fmt)
    assert isinstance(fmttime(time_to_fmt), int)


def test_prstime():
    timestamp_int = 1559290405

    with pytest.raises(TypeError) as exc_info:
        prstime('20190101T00:00:00')

    assert prstime(timestamp_int) == dt.datetime(1970, 1, 19, 1, 8, 10)
    assert isinstance(prstime(timestamp_int), dt.datetime)
    assert isinstance(exc_info.value, TypeError)


def test_current_date():
    now = dt.datetime.utcnow()
    assert current_date() == now - dt.timedelta(hours=now.hour, minutes=now.minute,
                                                seconds=now.second, microseconds=now.microsecond)
    assert current_date() != dt.datetime.now()


def test_days_to_timedelta():
    yesterday = dt.timedelta(days=1)
    assert yesterday == days_to_timedelta(1)
    assert yesterday != days_to_timedelta(2)

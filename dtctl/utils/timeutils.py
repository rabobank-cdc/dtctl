"""Common functions for DateTime related actions"""
import datetime as dt


def utc_now_timestamp():
    """
    Helper function to return textual representation of utcnow()

    :return: Current UTC time in textual format
    :rtype: String
    """
    return dt.datetime.utcnow().isoformat()


def determine_date_range(days, end_date, start_date):
    """
    Helper function to return correct start and end dates

    :return: DateTime tuple: DateTime objects for end_date and start_date
    """
    if not start_date:
        if days >= 0:
            start_date = current_date() - days_to_timedelta(days)
    if not end_date:
        end_date = current_date()
    end_date += dt.timedelta(hours=23, minutes=59, seconds=59)
    return end_date, start_date


def fmttime(time_to_fmt):
    """
    Helper function to format datetime to epoch. If already an int, doesn't do any formatting.

    :return: int: Time in epoch
    """
    if isinstance(time_to_fmt, int):
        return time_to_fmt
    return round(time_to_fmt.timestamp() * 1000)


def prstime(time_to_parse, iso=False):
    """
    Helper function to convert epoch to DateTime

    :param time_to_parse: Time in epoc to parse
    :type time_to_parse: int
    :param iso: Flag to signal output format
    :type iso: Boolean
    :return: DateTime
    """
    parsed_time = dt.datetime.utcfromtimestamp(round(time_to_parse / 1000))
    if iso:
        return parsed_time.isoformat()
    return parsed_time


def current_date():
    """
    Helper function to return current date

    :return: datetime: current date
    """
    now = dt.datetime.utcnow()
    today = now - dt.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    return today


def days_to_timedelta(nr_of_days):
    """
    Helper function to convert number of days to TimeDelta

    :return: TimeDelta
    """
    return dt.timedelta(days=int(nr_of_days))

"""Common functions for parsing and conversion requirements"""
import json


def convert_json_to_log_lines(output, timestamp_key='timestamp', system_key='system'):
    """
    Function to convert a list of JSON objects to a list containing log lines

    :param output: List of flat JSON objects (dicts within python)
    :type output: List
    :param timestamp_key: The dictionary key that holds timestamp information
    :type timestamp_key: String
    :param system_key: The dictionary key that holds the identifier for the system generating the log line
    :type system_key: String
    :return: JSON object converted to separate log lines
    :rtype: List
    """
    # Example of our goal log line
    # [2019-01-01T00:00:00.123456] system key1=value key2=value keyN=value

    if not isinstance(output, list):
        raise TypeError('Not a list')

    log_lines = []
    for line in output:
        timestamp = line.pop(timestamp_key)
        system_name = line.pop(system_key)
        message = ''
        for key, value in line.items():
            if isinstance(value, (list, dict, set)):
                raise TypeError('Nested objects are not supported')
            message += ' {0}={1}'.format(key, json.dumps(value))

        log_lines.append('[{ts}] {system}{message}\n'.format(ts=timestamp, system=system_name, message=message))
    return log_lines


def convert_series(series_to_convert):
    """
    Convert pandas Series to comma separated string

    :param series_to_convert: The pandas Series to convert
    :type series_to_convert: Series
    :return: Comma separated string or None
    :rtype: String
    """
    if isinstance(series_to_convert, list):
        if series_to_convert:
            return ', '.join(series_to_convert)
        return None
    return None

import json
from datetime import datetime as dt
from dtctl.utils.timeutils import fmttime


def convert_json_to_cef(output, timestamp_key='timestamp', system_key='system'):
    """
    Function to convert a list of JSON objects to a list containing CEF log lines

    :param output: List of flat JSON objects (dicts within python)
    :type output: List
    :param timestamp_key: The dictionary key that holds timestamp information
    :type timestamp_key: String
    :param system_key: The dictionary key that holds the identifier for the system generating the log line
    :type system_key: String
    :return: JSON object converted to separate log lines
    :rtype: List
    """
    # CEF format
    # CEF:Version|Device Vendor|Device Product|Device Version|Device Event Class ID|Name|Severity|[Extension]

    # CEF Example
    # CEF:0|Security|threatmanager|1.0|100|worm successfully stopped|10|src=10.0.0.1 dst=2.1.2.2 spt=1232

    if not isinstance(output, list):
        raise TypeError('Not a list')

    log_lines = []
    for json_object in output:
        timestamp = fmttime(dt.strptime(json_object.pop(timestamp_key), '%Y-%m-%dT%H:%M:%S'), False)
        system_name = json_object.pop(system_key)
        cef_log_line = \
            'CEF:0|Darktrace|DCIP System Monitoring|1.0|100|system usage|5|start={0} end={0} src={1} '\
            .format(timestamp, system_name)
        cef_log_line += '{0}\n'.format(convert_to_custom_cef_fields(json_object))
        log_lines.append(cef_log_line)
    return log_lines


def convert_to_custom_cef_fields(input_dict):
    """
    Function to convert a dictionary to a CEF compatible string
    with DeviceCustom fields.

    :param input_dict: Dictionary containing Key Value pairs in need of conversion
    :type input_dict: Dict
    :return: The CEF Extension string with DeviceCustom fields
    :rtype: String
    """
    string_counter = 0
    float_counter = 0
    number_counter = 0
    line = ''

    for key, value in input_dict.items():
        if isinstance(value, (list, dict, set)):
            raise TypeError('Nested objects are not supported')

        key = escape_strings_for_cef(key)
        value = escape_strings_for_cef(value)

        if isinstance(value, str):
            string_counter += 1
            line += 'cs{counter}Label={k} cs{counter}={v} '.format(counter=string_counter, v=value, k=key)

        elif isinstance(value, float):
            float_counter += 1
            line += 'cf{counter}Label={k} cf{counter}={v} '.format(counter=float_counter, v=value, k=key)

        elif isinstance(value, int):
            number_counter += 1
            line += 'cn{counter}Label={k} cn{counter}={v} '.format(counter=number_counter, v=value, k=key)

    return line.strip()


def escape_strings_for_cef(line):
    """
    Function to escape strings to be CEF compatible

    The characters "\" and "=" need to be escaped

    :param line: The text for which characters need to be replaced
    :type line: String
    :return: Text with characters escaped
    :rtype: String
    """
    if isinstance(line, str):
        return line.translate(str.maketrans({
            '=': r'\=',
            '\\': '\\\\'
        }))

    return line


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

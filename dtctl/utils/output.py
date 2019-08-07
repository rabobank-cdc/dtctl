"""Common functions for output related requirements"""
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


def process_output(output, outfile, append=False, to_json=True):
    """
    Output a Python object (Dict or List) to stdout or file

    :param output: The data to output
    :type output: Dict or List
    :param outfile: The file to write the output to
    :type outfile: String
    :param append: Flag for appending to file
    :type append: Boolean
    :param to_json: Flag for outputting in json
    :type append: Boolean
    :return: None
    :rtype: None
    """
    if not output:
        raise SystemExit('Error: No output to write or display')

    # Process the output for when an outfile is specified
    if outfile:
        file_mode = 'a' if append else 'w'

        with open(outfile, file_mode) as ofile:
            if to_json:
                json.dump(output, ofile, indent=4, sort_keys=True)
            else:
                ofile.writelines(output)
        return

    # Process the output for printing to screen for json objects
    if to_json:
        print(json.dumps(output, indent=4))
        return

    # Process the output for printing to screen for iterables
    if isinstance(output, (list, set)):
        for item in output:
            print(str(item).strip())
    else:
        print(output)


def make_curl_command(prepared_request):
    """
    Turn a prepared Request into a curl command.
    Generally used for debugging purposes

    :param prepared_request: Prepared Request
    :type prepared_request: Request
    :return: Curl command string
    :rtype: String
    """
    command = "curl -i -X {method} -H {headers} --insecure -d \"{data}\" \"{uri}\""
    method = prepared_request.method
    uri = prepared_request.url
    data = prepared_request.body
    headers = ['"{0}: {1}"'.format(key, value) for key, value in prepared_request.headers.items()]
    headers = " -H ".join(headers)
    return command.format(method=method, headers=headers, data=data, uri=uri)

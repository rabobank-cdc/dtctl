"""Common functions for output related requirements"""
import json


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


def process_output(output, outfile):
    """
    Output a Python object (Dict or List) to stdout or file

    :param output: The data to output
    :type output: Dict or List
    :param outfile: The file to write the output to
    :type outfile: String
    :return: None
    :rtype: None
    """
    if output:
        if outfile:
            with open(outfile, 'w') as ofile:
                json.dump(output, ofile, indent=4, sort_keys=True)

        else:
            try:
                print(json.dumps(output, indent=4))
            except json.JSONDecodeError:
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

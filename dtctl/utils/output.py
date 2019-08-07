"""Common functions for output related requirements"""
import json
from datetime import datetime as dt


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

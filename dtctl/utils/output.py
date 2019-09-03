"""Common functions for output related requirements"""
import json
import click


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
        # We raise it as SystemExit instead of click.UsageError
        # because it is not necessarily an error to not have output
        # however, we do want an exit code != 0
        raise SystemExit('No output to write or display')

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


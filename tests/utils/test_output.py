import os
import json
import pytest
from dtctl.utils.output import convert_json_to_log_lines, convert_series, process_output


def test_convert_series():
    # This function does not really convert Pandas series but only lists.
    test_data = ['a', 'b', 'c']

    assert convert_series(test_data) == 'a, b, c'
    assert convert_series('text') is None
    assert convert_series([]) is None


def test_process_output(tmpdir, capsys):
    tmpfile = '{0}/pytest.tmp.json'.format(tmpdir)

    output = {
        'key1': [1, 2, 3],
        'key2': 'data',
        'key3': {
            'subkey1': ['value1', 'value2'],
            'subkey2': True
        }
    }
    process_output(output, tmpfile)

    assert os.path.isfile(tmpfile)

    with open(tmpfile) as infile:
        loaded_output_file = json.load(infile)

    assert loaded_output_file['key1'][0] == 1
    assert loaded_output_file['key1'][1] == 2
    assert loaded_output_file['key1'][2] == 3
    assert loaded_output_file['key2'] == 'data'
    assert loaded_output_file['key3']['subkey1'][0] == 'value1'
    assert loaded_output_file['key3']['subkey1'][1] == 'value2'
    assert loaded_output_file['key3']['subkey2']

    process_output(output, None)

    captured = capsys.readouterr()
    assert '{\n    "key1": [\n        1,\n' in captured.out
    assert '"key2": "data",\n' in captured.out
    assert '"key3": {\n' in captured.out
    assert '"subkey2": true\n    }' in captured.out

    if os.path.isfile(tmpfile):
        os.remove(tmpfile)


def test_process_output_to_log(capsys):
    output = [
        "[2019-01-01T00:00:01] 1.1.1.1 key=\"value\"",
        "[2019-01-01T00:00:02] 1.1.1.2 key=\"value\"",
        "[2019-01-01T00:00:03] 1.1.1.3 key=\"value\"",
        "[2019-01-01T00:00:04] 1.1.1.4 key=\"value\""
    ]
    append = False
    to_json = False

    process_output(output, None, to_json, append)

    captured = capsys.readouterr()
    assert '[2019-01-01T00:00:03] 1.1.1.3 key="value"' in captured.out


def test_convert_json_to_log_lines():
    output = [
        {
            "system": "system1",
            "timestamp": "2019-01-01T00:00:01",
            "key1": "value1",
            "key2": "value2"
        },
        {
            "system": "system2",
            "timestamp": "2019-01-01T00:00:02",
            "key1": "value1",
            "key2": "value2"
        },
        {
            "system": "system3",
            "timestamp": "2019-01-01T00:00:03",
            "key1": "value1",
            "key2": "value2"
        }
    ]

    failing_output = [
        {
            "system": "system1",
            "timestamp": "2019-01-01T00:00:01",
            "key1": [1, 2, 3],
            "key2": "value2"
        }
    ]

    with pytest.raises(TypeError) as exc_info:
        convert_json_to_log_lines('This is not a list')

    assert isinstance(exc_info.value, TypeError)

    converted_output = convert_json_to_log_lines(output)

    assert converted_output[0].strip() == '[2019-01-01T00:00:01] system1 key1="value1" key2="value2"'
    assert converted_output[1].strip() == '[2019-01-01T00:00:02] system2 key1="value1" key2="value2"'
    assert converted_output[2].strip() == '[2019-01-01T00:00:03] system3 key1="value1" key2="value2"'

    with pytest.raises(TypeError) as exc_info:
        convert_json_to_log_lines(failing_output)

    assert isinstance(exc_info.value, TypeError)

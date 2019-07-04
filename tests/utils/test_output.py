import os
import json
from dtctl.utils.output import convert_series, process_output


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

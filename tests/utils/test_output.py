import os
import json
import pytest
from dtctl.utils.output import process_output


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


def test_process_output_to_cef(capsys):
    output = [
        "CEF:0|DCIP|System Monitoring|1.0|100|system usage|5|start=1234567890 end=1234567890 src=10.10.10.1 "
        "cs1Label=type cs1=probe cs2Label=label cs2=Appliance label1 cn1Label=bandwidth cn1=1000 cn2Label=cpu cn2=50",
        "CEF:0|DCIP|System Monitoring|1.0|100|system usage|5|start=1234567890 end=1234567890 src=10.10.10.2 "
        "cs1Label=type cs1=master cs2Label=label cs2=Appliance label2 cn1Label=bandwidth cn1=1000 cn2Label=cpu cn2=50",
    ]
    append = False
    to_json = False

    process_output(output, None, to_json, append)

    captured = capsys.readouterr()
    print(captured.out)
    assert 'CEF:0|DCIP|System Monitoring|1.0|100|system usage|5|' \
           'start=1234567890 end=1234567890 src=10.10.10.1 cs1Label=type cs1=probe ' \
           'cs2Label=label cs2=Appliance label1 cn1Label=bandwidth cn1=1000 cn2Label=cpu cn2=50' in captured.out
    assert 'CEF:0|DCIP|System Monitoring|1.0|100|system usage|5|' \
           'start=1234567890 end=1234567890 src=10.10.10.2 cs1Label=type cs1=master ' \
           'cs2Label=label cs2=Appliance label2 cn1Label=bandwidth cn1=1000 cn2Label=cpu cn2=50' in captured.out

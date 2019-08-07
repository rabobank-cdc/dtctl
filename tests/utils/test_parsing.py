import pytest
from dtctl.utils.parsing import convert_json_to_log_lines, convert_json_to_cef, convert_series


@pytest.fixture
def correct_output():
    return [
        {
            "system": "system1",
            "timestamp": "2019-01-01T00:00:01",
            "key1": "value1",
            "key2": 2
        },
        {
            "system": "system2",
            "timestamp": "2019-01-01T00:00:02",
            "key1": "value1",
            "key2": 2.123
        },
        {
            "system": "system3",
            "timestamp": "2019-01-01T00:00:03",
            "key1": "value1",
            "key2": 2
        },
        {
            "system": "system4",
            "timestamp": "2019-01-01T00:00:04",
            "key1": "value1",
            "key2": "value2",
            "key3": 3,
            "key4": 4
        }
    ]


@pytest.fixture
def failing_output():
    return [
        {
            "system": "system1",
            "timestamp": "2019-01-01T00:00:01",
            "key1": [1, 2, 3],
            "key2": "value2"
        }
    ]


def test_convert_series():
    # This function does not really convert Pandas series but only lists.
    test_data = ['a', 'b', 'c']

    assert convert_series(test_data) == 'a, b, c'
    assert convert_series('text') is None
    assert convert_series([]) is None


def test_convert_json_to_cef(correct_output, failing_output):
    with pytest.raises(TypeError) as exc_info:
        convert_json_to_cef('This is not a list')

    assert isinstance(exc_info.value, TypeError)

    converted_output = convert_json_to_cef(correct_output)

    assert converted_output[0].strip() == 'CEF:0|Darktrace|DCIP System Monitoring|1.0|100|system usage|5|' \
                                          'start=1546297201 end=1546297201 src=system1 ' \
                                          'cs1Label=key1 cs1=value1 cn1Label=key2 cn1=2'
    assert converted_output[1].strip() == 'CEF:0|Darktrace|DCIP System Monitoring|1.0|100|system usage|5|' \
                                          'start=1546297202 end=1546297202 src=system2 ' \
                                          'cs1Label=key1 cs1=value1 cf1Label=key2 cf1=2.123'
    assert converted_output[3].strip() == 'CEF:0|Darktrace|DCIP System Monitoring|1.0|100|system usage|5|' \
                                          'start=1546297204 end=1546297204 src=system4 ' \
                                          'cs1Label=key1 cs1=value1 cs2Label=key2 cs2=value2 ' \
                                          'cn1Label=key3 cn1=3 cn2Label=key4 cn2=4'

    with pytest.raises(TypeError) as exc_info:
        convert_json_to_cef(failing_output)

    assert isinstance(exc_info.value, TypeError)


def test_convert_json_to_log_lines(correct_output, failing_output):
    with pytest.raises(TypeError) as exc_info:
        convert_json_to_log_lines('This is not a list')

    assert isinstance(exc_info.value, TypeError)

    converted_output = convert_json_to_log_lines(correct_output)

    assert converted_output[0].strip() == '[2019-01-01T00:00:01] system1 key1="value1" key2=2'
    assert converted_output[1].strip() == '[2019-01-01T00:00:02] system2 key1="value1" key2=2.123'
    assert converted_output[2].strip() == '[2019-01-01T00:00:03] system3 key1="value1" key2=2'

    with pytest.raises(TypeError) as exc_info:
        convert_json_to_log_lines(failing_output)

    assert isinstance(exc_info.value, TypeError)

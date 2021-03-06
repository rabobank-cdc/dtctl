import pytest
from dtctl.utils.cef import Cef


@pytest.fixture
def correct_output():
    return [
        {
            "system": "system1",
            "ip": "10.0.0.1",
            "timestamp": "2019-01-01T00:00:01",
            "key1": "value1",
            "key2": 2
        },
        {
            "system": "system2",
            "ip": "10.0.0.2",
            "timestamp": "2019-01-01T00:00:02",
            "key1": "value1",
            "key2": 2.123
        },
        {
            "system": "system3",
            "ip": "10.0.0.3",
            "timestamp": "2019-01-01T00:00:03",
            "key1": "value1",
            "key2": 2
        },
        {
            "system": "system4",
            "ip": "10.0.0.4",
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
            "ip": "10.0.0.1",
            "timestamp": "2019-01-01T00:00:01",
            "key1": [1, 2, 3],
            "key2": "value2"
        }
    ]


def test_cef_creation():
    cef = Cef(1, 'name')

    assert cef.version == 0
    assert cef.vendor == 'Darktrace'
    assert cef.product == 'DCIP System Monitoring'
    assert cef.device_version == '1.0'
    assert cef.severity == 3
    assert cef.name == 'name'
    assert cef.device_event_class_id == 1

    cef = Cef(1, 'name', 5)
    assert cef.severity == 5


def test_convert_to_custom_cef_fields(correct_output, failing_output):
    cef = Cef(100, 'System Usage')

    converted_output = cef.convert_to_custom_cef_fields(correct_output[0])
    assert converted_output == 'cs1Label=system cs1=system1 cs2Label=ip cs2=10.0.0.1 cs3Label=timestamp ' \
                               'cs3=2019-01-01T00:00:01 cs4Label=key1 cs4=value1 cn1Label=key2 cn1=2'

    converted_output = cef.convert_to_custom_cef_fields(correct_output[2])
    assert converted_output == 'cs1Label=system cs1=system3 cs2Label=ip cs2=10.0.0.3 cs3Label=timestamp ' \
                               'cs3=2019-01-01T00:00:03 cs4Label=key1 cs4=value1 cn1Label=key2 cn1=2'

    with pytest.raises(TypeError) as exc_info:
        cef.convert_to_custom_cef_fields(failing_output[0])
    assert isinstance(exc_info.value, TypeError)


def test_escape_strings_for_cef():
    cef = Cef(100, 'System Usage')

    assert cef.escape_strings_for_cef(1) == 1
    assert cef.escape_strings_for_cef(r'test') == 'test'
    assert cef.escape_strings_for_cef(r'test=test') == r'test\=test'
    assert cef.escape_strings_for_cef(r'test\test') == r'test\\test'


def test_generate_logs_for_system_usage():
    cef = Cef(100, 'System Usage')
    output = [
        {
            "system": "system1",
            "ip": "10.0.0.1",
            "type": "master",
            "timestamp": "2019-01-01T01:01:01",
            "label": "Master machine",
            "bandwidth": 1000000000,
            "memused": 10,
            "connectionsPerMinuteCurrent": 1000,
            "cpu": 10
        }
    ]

    cef_logging = cef.generate_logs(output)
    assert cef_logging[0].strip() == 'CEF:0|Darktrace|DCIP System Monitoring|1.0|100|System Usage|3|' \
                                     'end=Jan 01 2019 01:01:01 deviceExternalId=system1 dvc=10.0.0.1 cs1Label=type ' \
                                     'cs1=master cs2Label=label cs2=Master machine cs3Label=bandwidth cs3=1000000000 ' \
                                     'cs4Label=memused cs4=10 cs5Label=connectionsPerMinuteCurrent cs5=1000 ' \
                                     'cs6Label=cpu cs6=10'

    with pytest.raises(TypeError) as exc_info:
        cef.generate_logs('Not a list')
    assert isinstance(exc_info.value, TypeError)


def test_generate_logs_for_packet_loss():
    cef = Cef(110, 'Packet Loss')
    output = [
        {
            "system": "system1",
            "ip": "10.0.0.1",
            "timestamp": "2019-01-01T01:01:01",
            "packet_loss": 10.000,
            "worker_drop_rate": 0.001
        }
    ]

    cef_logging = cef.generate_logs(output)
    assert cef_logging[0].strip() == 'CEF:0|Darktrace|DCIP System Monitoring|1.0|110|Packet Loss|3|' \
                                     'end=Jan 01 2019 01:01:01 deviceExternalId=system1 dvc=10.0.0.1 ' \
                                     'cs1Label=packet_loss cs1=10.0 cs2Label=worker_drop_rate cs2=0.001'

    with pytest.raises(TypeError) as exc_info:
        cef.generate_logs('Not a list')
    assert isinstance(exc_info.value, TypeError)


def test_generate_logs_for_dhcp():
    cef = Cef(120, 'DHCP Quality', 4)
    output = [
        {
            "system": "system1",
            "timestamp": "2019-01-01T01:01:01",
            "subnets_not_registered": 0,
            "subnets_seen": 10,
            "subnets_with_dhcp_disabled": 1,
            "subnets_without_clients": 2,
            "subnets_failing_dhcp": 3,
            "subnets_tracking_dhcp": 4,
            "total_dhcp_quality": 100,
            "average_dhcp_quality": 25
        }
    ]

    cef_logging = cef.generate_logs(output)
    assert cef_logging[0].strip() == 'CEF:0|Darktrace|DCIP System Monitoring|1.0|120|DHCP Quality|4|' \
                                     'end=Jan 01 2019 01:01:01 deviceExternalId=system1 ' \
                                     'cs1Label=subnets_tracking_dhcp cs1=4 cs2Label=total_dhcp_quality cs2=100 ' \
                                     'cs3Label=average_dhcp_quality cs3=25'
    assert 'dvc=' not in cef_logging[0]

    with pytest.raises(TypeError) as exc_info:
        cef.generate_logs('Not a list')
    assert isinstance(exc_info.value, TypeError)


def test_generate_logs_for_system_issue():
    cef = Cef(130, 'System Issue', 5)
    output = [
        {
            "system": "system1",
            "timestamp": "2019-01-01T01:01:01",
            "message": "Probe 10.0.0.1 has problem x",
        }
    ]

    cef_logging = cef.generate_logs(output)
    assert cef_logging[0].strip() == 'CEF:0|Darktrace|DCIP System Monitoring|1.0|130|System Issue|5|' \
                                     'end=Jan 01 2019 01:01:01 deviceExternalId=system1 ' \
                                     'msg=Probe 10.0.0.1 has problem x'

    with pytest.raises(TypeError) as exc_info:
        cef.generate_logs('Not a list')
    assert isinstance(exc_info.value, TypeError)


def test_cef_mapping():
    cef = Cef(100, 'System Usage')
    assert len(cef.MAPPING) == 5
    assert len(cef.MAPPING['System Usage']) == 7
    assert len(cef.MAPPING['Packet Loss']) == 2
    assert len(cef.MAPPING['DHCP Quality']) == 3
    assert len(cef.MAPPING['System Issue']) == 1

    assert cef.MAPPING['System Usage']['type'] == 'cs1Label'
    assert cef.MAPPING['System Usage']['label'] == 'cs2Label'
    # assert cef.MAPPING['System Usage']['bandwidth'] == 'in'
    assert cef.MAPPING['System Usage']['bandwidth'] == 'cs3Label'
    # assert cef.MAPPING['System Usage']['memused'] == 'cn1Label'
    assert cef.MAPPING['System Usage']['memused'] == 'cs4Label'
    # assert cef.MAPPING['System Usage']['connectionsPerMinuteCurrent'] == 'cn2Label'
    assert cef.MAPPING['System Usage']['connectionsPerMinuteCurrent'] == 'cs5Label'
    # assert cef.MAPPING['System Usage']['cpu'] == 'cn3Label'
    assert cef.MAPPING['System Usage']['cpu'] == 'cs6Label'
    # assert cef.MAPPING['System Usage']['dtqueue'] == 'flexNumber1Label'
    assert cef.MAPPING['System Usage']['dtqueue'] == 'flexString1Label'

    assert cef.MAPPING['Packet Loss']['packet_loss'] == 'cs1Label'
    assert cef.MAPPING['Packet Loss']['worker_drop_rate'] == 'cs2Label'

    # assert cef.MAPPING['DHCP Quality']['subnets_tracking_dhcp'] == 'cn1Label'
    assert cef.MAPPING['DHCP Quality']['subnets_tracking_dhcp'] == 'cs1Label'
    # assert cef.MAPPING['DHCP Quality']['total_dhcp_quality'] == 'cn2Label'
    assert cef.MAPPING['DHCP Quality']['total_dhcp_quality'] == 'cs2Label'
    # assert cef.MAPPING['DHCP Quality']['average_dhcp_quality'] == 'cn3Label1'
    assert cef.MAPPING['DHCP Quality']['average_dhcp_quality'] == 'cs3Label'

    assert cef.MAPPING['System Issue']['message'] == 'msg'

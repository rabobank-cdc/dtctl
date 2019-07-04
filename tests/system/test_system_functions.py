import json
import pytest
from unittest.mock import MagicMock
from dtctl.system.functions import get_instances, get_info, get_usage
from dtctl.dtapi.api import Api


@pytest.fixture
def status_info():
    data_file = 'tests/data/status.json'
    with open(data_file) as infile:
        json_data = json.load(infile)
    return json_data


def test_get_info():
    data_file = 'tests/data/time.json'
    with open(data_file) as infile:
        json_data = json.load(infile)

    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=json_data)

    result = get_info(api)

    assert json_data['antigena'] == result['antigena']
    assert json_data['antigenainternet'] == result['antigenainternet']
    assert json_data['antigenanetwork'] == result['antigenanetwork']
    assert json_data['build'] == result['build']
    assert json_data['inoculation'] == result['inoculation']
    assert json_data['mobileAppConfigured'] == result['mobileAppConfigured']
    assert json_data['time'] == result['time']
    assert json_data['timems'] == result['timems']
    assert json_data['uptime'] == result['uptime']
    assert json_data['version'] == result['version']


def test_get_instances(status_info):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=status_info)

    instances = get_instances(api)

    assert instances['darktrace-instance-1']['id'] == 1
    assert instances['darktrace-instance-1']['label'] == 'Label with a name1'
    assert 'region' not in instances['darktrace-instance-1']
    assert instances['darktrace-instance-2']['id'] == 2
    assert instances['darktrace-instance-2']['label'] == 'Location2 - Name2'
    assert instances['darktrace-instance-2']['location'] == 'Location2'


def test_get_usage(status_info):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=status_info)

    result = get_usage(api)
    assert result['darktrace-instance-1']['cpu'] == 10
    assert result['darktrace-instance-1']['dtqueue'] == 0
    assert result['darktrace-instance-1']['memused'] == 10
    assert result['darktrace-instance-1']['bandwidth'] == 1000000000
    assert result['darktrace-instance-1']['connectionsPerMinuteCurrent'] == 100
    assert result['darktrace-instance-1']['label'] == 'Label with a name1'
    assert len(result['darktrace-instance-1']['probes']) == 1
    assert result['darktrace-instance-1']['probes']['192.168.1.1']['label'] == 'Label with a name1'
    assert result['darktrace-instance-1']['probes']['192.168.1.1']['bandwidthCurrent'] == 100000000
    assert result['darktrace-instance-1']['probes']['192.168.1.1']['memoryUsed'] == 10
    assert result['darktrace-instance-1']['probes']['192.168.1.1']['connectionsPerMinuteCurrent'] == 10
    assert result['darktrace-instance-1']['probes']['192.168.1.1']['cpu'] == 2
    assert len(result['darktrace-instance-2']['probes']) == 2

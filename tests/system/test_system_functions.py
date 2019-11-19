import json
import pytest
import ipaddress
from unittest.mock import MagicMock
from dtctl.system.functions import get_instances, get_info, get_usage, get_subnets_from_csv_file, \
    get_subnets_from_text_file
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

    instances = get_instances(api, True)

    assert instances['darktrace-instance-1']['id'] == 1
    assert instances['darktrace-instance-1']['label'] == 'Label with a name1'
    assert len(instances['darktrace-instance-1']['probes']) == 1
    assert instances['darktrace-instance-1']['probes'][0]['ip'] == '192.168.1.1'
    assert 'region' not in instances['darktrace-instance-1']
    assert instances['darktrace-instance-2']['id'] == 2
    assert instances['darktrace-instance-2']['label'] == 'Location2 - Name2'
    assert instances['darktrace-instance-2']['location'] == 'Location2'
    assert instances['darktrace-instance-2']['probes'][2]['error']
    assert instances['darktrace-instance-3']['error']


def test_get_usage(status_info):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=status_info)

    result = get_usage(api)

    assert len(result) == 6

    assert result[0]['system'] == 'darktrace-hostname-1'
    assert result[0]['type'] == 'master'
    assert result[0]['timestamp']
    assert result[0]['cpu'] == 10
    assert result[0]['dtqueue'] == 0
    assert result[0]['memused'] == 10
    assert result[0]['bandwidth'] == 1000000000
    assert result[0]['connectionsPerMinuteCurrent'] == 100
    assert result[0]['label'] == 'Label with a name1'

    assert result[1]['system'] == 'probe-hostname-1'
    assert result[1]['ip'] == '192.168.1.1'
    assert result[1]['type'] == 'probe'
    assert result[1]['timestamp']
    assert result[1]['cpu'] == 2
    assert result[1]['memused'] == 10
    assert result[1]['bandwidth'] == 100000000
    assert result[1]['connectionsPerMinuteCurrent'] == 10
    assert result[1]['label'] == 'Label with a name1'
    assert 'dtqueue' not in result[1]  # probes don't have dtqueue


def test_get_subnets_from_csv_file():
    infile_sample = 'tests/data/subnet_input_list.csv'

    subnets = get_subnets_from_csv_file(infile_sample, 'network', 'netmask')
    for subnet in subnets:  # set with one element
        assert isinstance(subnet, ipaddress.IPv4Network)
        assert str(subnet) == '10.0.0.0/24'


def test_get_subnets_from_txt_file():
    infile_sample = 'tests/data/subnet_input_list.txt'

    subnets = get_subnets_from_text_file(infile_sample)
    i = 0
    for subnet in subnets:  # set with two element
        assert isinstance(subnet, ipaddress.IPv4Network)
        assert str(subnet) == '10.{0}.0.0/24'.format(i)
        i += 1

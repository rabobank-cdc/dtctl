import json
import pytest
from unittest.mock import MagicMock
from dtctl.devices.functions import get_device_info, get_devices
from dtctl.dtapi.api import Api


@pytest.fixture
def devices():
    data_file = 'tests/data/devices.json'
    with open(data_file) as infile:
        json_data = json.load(infile)
    return json_data


def test_get_devices(devices):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=devices)

    result = get_devices(api, None, 3600)

    assert len(result) == 3
    assert 'ips' in result[0]
    assert result[0]['ip'] == '10.0.0.10'
    assert result[0]['typename'] == 'desktop'

    assert 'credentials' in result[1]
    assert result[1]['typename'] == 'laptop'
    assert result[1]['hostname'] == 'testdevice.domain.dev'

    assert len(result[2]['ips']) == 1
    assert result[2]['typename'] == 'server'
    assert result[2]['credentials'][0]['credential'] == 'testCredential2'

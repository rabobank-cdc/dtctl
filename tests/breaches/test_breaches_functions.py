import json
import pytest
from unittest.mock import MagicMock
from dtctl.breaches.functions import has_enhanced_tag, get_instances_region
from dtctl.dtapi.api import Api


@pytest.fixture
def status_info():
    data_file = 'tests/data/status.json'
    with open(data_file) as infile:
        json_data = json.load(infile)
    return json_data


def test_has_enhanced_tag():
    assert has_enhanced_tag(['test1', 'test2', 'enhanced monitoring']) == 1
    assert has_enhanced_tag(['test1', 'Test2', 'Enhanced Monitoring']) == 1
    assert has_enhanced_tag(['test1', 'test2', 'enhanced']) == 1
    assert has_enhanced_tag(['Enhanced Test', 'test1', 'test2']) == 1
    assert has_enhanced_tag([]) == 0
    assert has_enhanced_tag(['test1', 'test2']) == 0


def test_get_instances_region(status_info):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=status_info)

    instances = get_instances_region(api)

    assert instances[1]['label'] == 'Label with a name1'
    assert 'region' not in instances[1]
    assert instances[2]['label'] == 'Location2 - Name2'
    assert instances[2]['region'] == 'Location2'

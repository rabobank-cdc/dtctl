import json
import pytest
from unittest.mock import MagicMock
from dtctl.tags.functions import get_tags, modify_device_tags, search_tags
from dtctl.dtapi.api import Api


@pytest.fixture
def tags():
    data_file = 'tests/data/tags.json'
    with open(data_file) as infile:
        json_data = json.load(infile)
    return json_data


@pytest.fixture
def delete_responses():
    delete_responses = {
        400: {'status_code': 400, 'status': 'bad request'},
        404: {'status_code': 404, 'status': 'unknown'}  # default status for "unknown" status codes
    }

    for i in [200, 201, 202, 204]:
        delete_responses[i] = {
            'status_code': i,
            'status': 'success'
        }

    for i in [401, 403, 405, 409]:
        delete_responses[i] = {
            'status_code': i,
            'status': 'unauthorized'
        }

    for i in [501, 502]:
        delete_responses[i] = {
            'status_code': i,
            'status': 'error'
        }

    return delete_responses


def test_get_tags(tags):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=tags)

    result = get_tags(api)

    assert len(result) == 6
    assert result[3]['name'] == tags[3]['name']


def test_deletion_of_device_tag(delete_responses):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')

    for i in [200, 201, 202, 204]:
        api.delete = MagicMock(return_value=delete_responses[i])
        result = modify_device_tags(api, 'delete', 'Admin', '10000000')
        assert result['status_code'] == i
        assert result['status'] == 'success'

    for i in [401, 403, 405, 409]:
        api.delete = MagicMock(return_value=delete_responses[i])
        result = modify_device_tags(api, 'delete', 'Admin', '10000000')
        assert result['status_code'] == i
        assert result['status'] == 'unauthorized'

    for i in [501, 502]:
        api.delete = MagicMock(return_value=delete_responses[i])
        result = modify_device_tags(api, 'delete', 'Admin', '10000000')
        assert result['status_code'] == i
        assert result['status'] == 'error'


def test_addition_of_device_tag():
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.post = MagicMock(return_value=[
            {
                "teid": 1000000000000,
                "tehid": 1000000000001,
                "entityType": "Device",
                "entityValue": "1000000000005",
                "valid": True
            }
        ]
    )

    result = modify_device_tags(api, 'add', 'Admin', '1000000000005')
    assert result[0]['teid'] == 1000000000000


def test_search_tag_names(tags):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=tags)

    result = search_tags(api, 'A*', None)
    assert len(result) == 5

    result = search_tags(api, '*Threat', None)
    assert len(result) == 1
    assert result[0]['name'] == 'Active Threat'

    result = search_tags(api, 'Antigen?', None)
    assert len(result) == 1

    result = search_tags(api, 'Antigen*', None)
    assert len(result) == 2

    result = search_tags(api, 'Android D?vice', None)
    assert len(result) == 1
    assert result[0]['name'] == 'Android Device'


def test_search_tagged_devices():
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=[
        {
            "teid": 1000000000000,
            "tehid": 1000000000001,
            "entityType": "Device",
            "entityValue": "1000000000005",
            "valid": True
        }
    ])

    result = search_tags(api, None, 'Admin')
    assert len(result) == 1
import json
import pytest
from unittest.mock import MagicMock
from dtctl.intelfeed.functions import get_intelfeed, add_entry_to_intelfeed
from dtctl.dtapi.api import Api


@pytest.fixture
def watchlist():
    data_file = 'tests/data/watched_domains.json'
    with open(data_file) as infile:
        json_data = json.load(infile)
    return json_data


def test_get_intelfeed(watchlist):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.get = MagicMock(return_value=watchlist)

    watched_items = get_intelfeed(api)
    assert len(watched_items) == len(watchlist)
    assert watched_items[2] == watchlist[2]


def test_add_single_entry_to_intelfeed():
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.post = MagicMock(return_value={
        "response": "SUCCESS",
        "added": 1,
        "updated": 0
    })

    response = add_entry_to_intelfeed(api, 'additional.test.dev', None)

    assert response['response'] == 'SUCCESS'
    assert response['added'] == 1
    assert response['updated'] == 0

    response = add_entry_to_intelfeed(api, '400.1.1.1', None)
    assert response == 'Not a valid domain, hostname, ip address or file'

    response = add_entry_to_intelfeed(api, 'https://www.google.com', None)
    assert response == 'Not a valid domain, hostname, ip address or file'


def test_add_entries_from_file_to_intelfeed(watchlist):
    api = Api('http://127.0.0.1', 'pubkey', 'privkey')
    api.post = MagicMock(return_value={
        "response": "SUCCESS",
        "added": 1,
        "updated": 0
    })

    infile = 'tests/data/items_for_intelfeed.txt'

    results = add_entry_to_intelfeed(api, None, infile)

    assert results[0]['1.1.1.1']['response'] == 'SUCCESS'
    assert results[1]['2.2.2.2']['added'] == 1
    assert results[2]['3.3.3.3']['updated'] == 0
    assert results[5]['localhost.local']['response'] == 'SUCCESS'
    assert results[7]['https://www.notcorrect'] == 'Not a valid IPv4 address or domain name'
    assert results[8]['400.1.1.1'] == 'Not a valid IPv4 address or domain name'

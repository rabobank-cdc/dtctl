import json
import pytest
from dtctl.breaches.functions import get_hostname_or_ip, get_dest_hostname_or_ip


@pytest.fixture
def triggered_components():
    data_file = 'tests/data/triggered_components.json'
    with open(data_file) as infile:
        json_data = json.load(infile)
    return json_data


def test_get_hostname_or_ip(triggered_components):
    assert 'host1.name.local' == get_hostname_or_ip(triggered_components[0])
    assert '10.0.0.1' != get_hostname_or_ip(triggered_components[0])
    assert 'host2.name.local' != get_hostname_or_ip(triggered_components[1])
    assert '10.0.0.2' == get_hostname_or_ip(triggered_components[1])
    assert 'Unknown' == get_hostname_or_ip(triggered_components[2])


def test_get_dest_hostname_or_ip(triggered_components):
    assert 'destination.hostname.test' == get_dest_hostname_or_ip(triggered_components[0])
    assert '10.0.0.1' == get_dest_hostname_or_ip(triggered_components[1])
    assert 'Destination message' == get_dest_hostname_or_ip(triggered_components[2])
    assert '' == get_dest_hostname_or_ip(triggered_components[3])

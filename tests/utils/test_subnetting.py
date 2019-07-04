import pytest
from dtctl.utils.subnetting import is_valid_ipv4_address, is_valid_ipv4_network, is_valid_ipv6_address


def test_is_valid_ipv4_address():
    with pytest.raises(TypeError) as exc_info:
        is_valid_ipv4_address(10000000)

    assert isinstance(exc_info.value, TypeError)
    assert is_valid_ipv4_address('10.0.0.1')
    assert not is_valid_ipv4_address('Test')
    assert not is_valid_ipv4_address('10.0.0.0/24')


def test_is_valid_ipv4_network():
    with pytest.raises(AttributeError) as exc_info:
        is_valid_ipv4_network(10000000)

    assert isinstance(exc_info.value, AttributeError)
    assert is_valid_ipv4_network('10.0.0.0/24')
    assert is_valid_ipv4_network('10.0.0.0/24/24')
    assert is_valid_ipv4_network('10.0.0.1')
    assert not is_valid_ipv4_address('not_a_network')


def test_is_valid_ipv6_address():
    with pytest.raises(TypeError) as exc_info:
        is_valid_ipv6_address(10000000)

    assert isinstance(exc_info.value, TypeError)
    assert is_valid_ipv6_address('0000:1bad:babe:0000:0000:0000:0000:0000')
    assert is_valid_ipv6_address('0000:1bad:babe::')
    assert not is_valid_ipv6_address('Test')
    assert not is_valid_ipv6_address('10.0.0.1')

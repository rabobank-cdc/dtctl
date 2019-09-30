"""Common functions for subnetting related actions"""
import socket
import re


def is_valid_ipv4_address(address):
    """
    Check if string is a valid IPv4 address

    :param address: IP address to check
    :type address: String
    :return: True or False if address is valid IPv4 address
    :rtype: Boolean
    """
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False

    return True


def is_valid_ipv4_network(network):
    """
    Check if string is a valid IPv4 network

    :param network: IP network to check
    :type network: String
    :return: True of False if address is valid IPv4 network
    :rtype: Boolean
    """
    base_net = network.split('/')[0]

    try:
        socket.inet_pton(socket.AF_INET, base_net)
    except AttributeError:
        try:
            socket.inet_aton(base_net)
        except socket.error:
            return False
        return base_net.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True


def is_valid_ipv6_address(address):
    """
    Check if string is a valid IPv6 address

    :param address: IP address to check
    :type address: String
    :return: True of False if address is valid IPv6 address
    :rtype: Boolean
    """
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except socket.error:  # not a valid address
        return False
    return True


def is_valid_domain(entry):
    """
    Check if string somewhat looks like a domain

    :param entry: Hostname to check
    :type entry: String
    :return: True for a match, False if no match
    :rtype: Boolean
    """
    domain_regex = re.compile('^([a-z0-9]+(-[a-z0-9]+)*\\.)+[a-z]{2,}$')

    if domain_regex.match(entry):
        return True
    return False


def is_valid_hostname(entry):
    """
    Check if string somewhat looks like a hostname

    :param entry: Hostname to check
    :type entry: String
    :return: True for a match, False if no match
    :rtype: Boolean
    """
    hostname_regex = re.compile('^([a-z0-9](?:[a-z0-9-]*[a-z0-9]))$')

    if hostname_regex.match(entry):
        return True
    return False

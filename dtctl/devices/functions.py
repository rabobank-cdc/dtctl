# pylint: disable=C0325
"""Functions used by the Click devices subcommand"""


def get_devices(api, days, seconds):
    """
    Retrieves list of active devices identified by Darktrace. List of devices can be partitioned by days or seconds.

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param days: Number of days since now
    :type days: Int
    :param seconds: Number of seconds since now
    :type seconds: Int
    :return: Active devices
    :rtype: List
    """
    if days:
        seen_since = '{0}days'.format(days)

    # Seconds supersedes days
    if seconds:
        seen_since = seconds

    return api.get('/devices', seensince=seen_since)


def get_device_info(api, device_id, full_device_details):
    """
    Retrieve detailed information for a device

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param device_id: Device ID to retrieve information for
    :type device_id: Int
    :param full_device_details: Retrieve additional device details
    :type full_device_details: Boolean
    :return: Device details
    :rtype: Dict
    """
    return api.get('/deviceinfo', did=device_id, fulldevicedetails=str(full_device_details).lower())


def get_device_info_by_ip(api, ip, days):
    """
    Retrieve device information by querying Darktrace for an internal IP address

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param ip: IP address to retrieve device information for
    :type ip: String
    :param days: Search for device information since X days
    :type days: Int
    :return: Darktrace device information
    :rtype: Dict
    """
    if days:
        seen_since = '{0}days'.format(days)

    return api.get('/devices', ip=ip, seensince=seen_since)

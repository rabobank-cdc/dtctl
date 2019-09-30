# pylint: disable=C0325
"""Functions used by the Click details subcommand"""

import os.path
import click
from dtctl.utils.timeutils import fmttime
from dtctl.utils.subnetting import is_valid_ipv4_address


def get_device_details(api, did, start_date, end_date):
    """
    Retrieve details for a device id

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param did:
    :type did:
    :param start_date: Start date for date range filtering
    :type start_date: Datetime
    :param end_date: End date for date range filtering
    :type end_date: Datetime
    :return: Details for device id
    :rtype: Dict
    """
    start_time = fmttime(start_date) if start_date else None
    end_time = fmttime(end_date) if end_date else None

    details = api.get('/details', did=did, starttime=start_time, endtime=end_time)
    return details


def get_endpoint_details(api, host, infile):
    """
    Retrieve details for external IP addresses and hostnames.

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param host: External hostname to receive details for
    :type host: String
    :param infile: Input file with an endpoint on each line
    :type infile: String
    :return: Details for external host
    :rtype: Dict or List
    """
    if infile:
        if not os.path.isfile(infile):
            raise click.UsageError('Input file does not exist')

        details = []
        with open(infile) as input_list:
            for line in input_list.readlines():
                details.append(api.get('/endpointdetails', additionalinfo='true', devices='true', ip=line.strip()))
        return details

    if is_valid_ipv4_address(host):
        details = api.get('/endpointdetails', additionalinfo='true', devices='true', ip=host)
    else:
        details = api.get('/endpointdetails', additionalinfo='true', devices='true', hostname=host)

    return details


def get_host_details(api, hostname, start_date, end_date):
    """
    Retrieve details for an external hostname

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param hostname: External hostname to receive details for
    :type hostname: String
    :param start_date: Start date for date range filtering
    :type start_date: Datetime
    :param end_date: End date for date range filtering
    :type end_date: Datetime
    :return: Details for external hostname
    :rtype: Dict
    """
    start_time = fmttime(start_date) if start_date else None
    end_time = fmttime(end_date) if end_date else None

    details = api.get('/details', externalhostname=hostname, starttime=start_time, endtime=end_time)
    return details


def get_message_details(api, message, start_date, end_date):
    """
    Retrieve details for a message. Mostly used for credentials

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param message: Message to receive details for
    :type message: String
    :param start_date: Start date for date range filtering
    :type start_date: Datetime
    :param end_date: End date for date range filtering
    :type end_date: Datetime
    :return: Details for external hostname
    :rtype: Dict
    """
    start_time = fmttime(start_date) if start_date else None
    end_time = fmttime(end_date) if end_date else None

    details = api.get('/details', msg=message, starttime=start_time, endtime=end_time)
    return details


def get_breach_details(api, pbid):
    """
    Retrieve details for a breach.

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param pbid: Breach ID
    :type pbid: Int
    :return: Details for breach
    :rtype: Dict
    """
    details = api.get('/details', pbid=pbid)
    return details


def get_connection_details(api, connection_uid, start_date, end_date):
    """
    Retrieve details for a connection.

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param connection_uid: Connection UID
    :type connection_uid: Int
    :param start_date: Start date for date range filtering
    :type start_date: Datetime
    :param end_date: End date for date range filtering
    :type end_date: Datetime
    :return: Details for connection
    :rtype: Dict
    """
    start_time = fmttime(start_date) if start_date else None
    end_time = fmttime(end_date) if end_date else None

    details = api.get('/details', uid=connection_uid, starttime=start_time, endtime=end_time)
    return details

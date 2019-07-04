"""Functions used by the Click intelfeed subcommand"""
from dtctl.utils.subnetting import is_valid_ipv4_address, is_valid_domain


def get_intelfeed(api):
    """
    Retrieve Darktrace intelligence feed

    :param api: Valid and authenticated Darktrace API object
    :type api: Api
    :return: Entries on the Darktrace intelfeed list
    :rtype: Dict
    """
    return api.get('/intelfeed')


def add_entry_to_intelfeed(api, entry):
    """
    Add entry to Darktrace intelligence feed

    :param api: Valid and authenticated Darktrace API object
    :type api: Api
    :param entry: Entry to add to Darktrace intelligence feed
    :type entry: String
    :return: Response message
    :rtype: String
    """
    if is_valid_ipv4_address(entry) or is_valid_domain(entry):
        return api.post('/intelfeed', postdata={'addentry': entry}, addentry=entry)
    return 'Not a valid domain, hostname or ip address'

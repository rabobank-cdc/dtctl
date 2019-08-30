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


def add_entry_to_intelfeed(api, entry, infile):
    """
    Add entry to Darktrace intelligence feed

    :param api: Valid and authenticated Darktrace API object
    :type api: Api
    :param entry: Entry to add to Darktrace's intelligence feed
    :type entry: String
    :param infile: File containing one entry per line for addition to Darktrace's intelligence feed
    :type infile: String
    :return: Response message
    :rtype: String
    """
    if infile:
        results = []
        with open(infile, 'r') as input_file:
            for line in input_file.readlines():
                line = line.strip()
                if is_valid_ipv4_address(line) or is_valid_domain(line):
                    results.append({
                        line: api.post('/intelfeed', postdata={'addentry': line}, addentry=line)
                    })
                else:
                    results.append({
                        line: 'Not a valid IPv4 address or domain name'
                    })
        return results

    if entry:
        if is_valid_ipv4_address(entry) or is_valid_domain(entry):
            return api.post('/intelfeed', postdata={'addentry': entry}, addentry=entry)

    return 'Not a valid domain, hostname, ip address or file'

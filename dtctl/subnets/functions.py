"""Functions used by the Click subnets subcommand"""

import ipaddress
import socket
import netaddr
from dtctl.utils.subnetting import is_valid_ipv4_network
from dtctl.utils.timeutils import utc_now_timestamp


def list_devices(api):
    """
    List the number of devices seen by Darktrace. This is the cummulative
    number of all devices reported by the individual subnets seen by Darktrace.

    :param api: Darktrace API object with initialized config values
    :return: Dictionary that contains the nr of devices
    """
    status_dict = api.get('/status')
    result = {'clients': 0, 'servers': 0, 'total': 0}
    for _, instance_values in status_dict['instances'].items():
        try:
            if instance_values['error'] is True:
                continue
        except KeyError:
            pass

        for subnet in instance_values['subnetData']:
            if 'devices' in subnet:
                result['total'] += subnet['devices']
                result['servers'] += subnet['devices']
            if 'clientDevices' in subnet:
                result['total'] += subnet['clientDevices']
                result['clients'] += subnet['clientDevices']

    return result


def get_subnet_list(api):
    """
    List all subnets seen by Darktrace. If performed on unified viewer, lists all sbunets
    seen for all Instances and Probes

    :param api: Darktrace API object with initialized config values
    :return: List that contains unique subnets
    """
    subnets = api.get('/subnets')

    place_holder = set()
    for subnet in subnets:
        # Subnet entry
        # {
        #     'sid': 6000000009896, 'auto': True, 'dhcp': True, 'firstSeen': 1552551497000,
        #     'label': '10.117.80.0/24', 'lastSeen': 1552551497000, 'latitude': 52.09,
        #     'longitude': 5.12, 'network': '10.117.80.0/24', 'shid': 6000000016884,
        #     'uniqueHostnames': False, 'uniqueUsernames': False
        # }
        try:
            network = ipaddress.ip_network(subnet['network'])
        except ValueError:
            continue
        # This filters out IPv6 for which we are note interested right now
        # At a certain point we need to make this IPv6 compatible
        if isinstance(network, ipaddress.IPv4Network):
            place_holder.add(network)

    # return sorted(place_holder, key=lambda item: socket.inet_aton(item.split('/')[0]))
    return sorted(place_holder)


def get_aggregates(api):
    """
    A Function for aggregating and listing all subnets seen by DarkTrace

    :param api: A valid and active authenticated session with the DarkTrace API
    :return: List of CIDR aggregated subnets
    """
    subnets = api.get('/subnets')
    place_holder = set()
    for subnet in subnets:
        # Subnet entry
        # {
        #     'sid': 6000000009896, 'auto': True, 'dhcp': True, 'firstSeen': 1552551497000,
        #     'label': '10.117.80.0/24', 'lastSeen': 1552551497000, 'latitude': 52.09,
        #     'longitude': 5.12, 'network': '10.117.80.0/24', 'shid': 6000000016884,
        #     'uniqueHostnames': False, 'uniqueUsernames': False
        # }
        if is_valid_ipv4_network(subnet['network']):
            place_holder.add(subnet['network'])

    subnets_to_merge = sorted(place_holder, key=lambda item: socket.inet_aton(item.split('/')[0]))
    merged_subnets = netaddr.cidr_merge(subnets_to_merge)
    final_subnets = []
    for merged_subnet in merged_subnets:
        final_subnets.append(str(merged_subnet))

    return final_subnets


def get_subnets_per_instances(api):
    """
    Listing all subnets seen by DarkTrace per instance

    :param api: A valid and active authenticated session with the DarkTrace API
    :return: Dictionary of subnet information per instance
    """
    subnets_per_instance = {}

    status_result = api.get('/status')
    instances = status_result['instances']

    for name, instance_values in instances.items():
        subnets_per_instance[name] = []
        seen_subnets = instance_values['subnetData']
        for subnet in seen_subnets:
            if is_valid_ipv4_network(subnet['network']):
                subnets_per_instance[name].append(subnet['network'])

    return subnets_per_instance


def get_unidirectional_traffic(api):
    """
    Statistics for unidirectional traffic

    :param api: Darktrace API object with initialized config values
    :return: Dictionary that contains system information
    """
    status_dict = api.get('/status')
    unidirectional_traffic = {}

    for instance_key, instance_values in status_dict['instances'].items():
        try:
            if instance_values['error'] is True:
                continue
        except KeyError:
            pass

        unidirectional_traffic[instance_key] = {}
        unidirectional_traffic[instance_key]['master_recorded'] = instance_values['recentUnidirectionalConnections']
        unidirectional_traffic[instance_key]['total_seen_subnets'] = len(instance_values['subnetData'])
        unidirectional_traffic[instance_key]['average_subnets_reporting_unidirectional'] = 'NOTIMPLEMENTED'
        subnet_count_00_to_10 = 0
        subnet_count_10_to_40 = 0
        subnet_count_40_to_70 = 0
        subnet_count_70_to_100 = 0

        for subnet in instance_values['subnetData']:
            if 'recentUnidirectionalTrafficPercent' not in subnet:
                continue

            uni = int(subnet['recentUnidirectionalTrafficPercent'])
            if 0 < uni < 10:
                subnet_count_00_to_10 += 1
            elif 10 <= uni < 40:
                subnet_count_10_to_40 += 1
            elif 40 <= uni < 70:
                subnet_count_40_to_70 += 1
            elif uni >= 70:
                subnet_count_70_to_100 += 1

        unidirectional_traffic[instance_key]['0_to_10%'] = subnet_count_00_to_10
        unidirectional_traffic[instance_key]['10_to_40%'] = subnet_count_10_to_40
        unidirectional_traffic[instance_key]['40_to_70%'] = subnet_count_40_to_70
        unidirectional_traffic[instance_key]['70_to_100%'] = subnet_count_70_to_100

    return unidirectional_traffic


def get_dhcp_stats(api):
    """
    Overview of DHCP seen status for each subnet

    :param api: Darktrace API object with initialized config values
    :return: Dictionary that contains system information
    """
    status_dict = api.get('/status')
    all_subnets = api.get('/subnets')
    subnets_by_sid = convert_to_subnets_by_sid(all_subnets)
    dhcp_statistics = []

    for _instance_key, instance_values in status_dict['instances'].items():
        try:
            if instance_values['error'] is True:
                continue
        except KeyError:
            pass

        dhcp_information = {
            'system': instance_values['hostname'],
            # 'ip': instance_key,  # Replace with 'ip' key once made available in status output
            'timestamp': utc_now_timestamp(),
            'subnets_not_registered': 0,
            'subnets_seen': len(instance_values['subnetData']),
            'subnets_with_dhcp_disabled': 0,
            'subnets_without_clients': 0,
            'subnets_failing_dhcp': 0,
            'subnets_tracking_dhcp': 0,
            'total_dhcp_quality': 0
        }

        for subnet in instance_values['subnetData']:
            # If a seen subnet is not in the Darktrace subnet list
            # we continue on the next. This should not happen to often
            # and usually is a result of timing issues with internal
            # Darktrace updating mechanisms
            if subnet['sid'] not in subnets_by_sid:
                dhcp_information['subnets_not_registered'] += 1
                continue

            # Boolean value provided by Darktrace
            # False: Darktrace does not track DHCP for this subnet
            # True: Darktrace tracks DHCP for this subnet
            if not subnets_by_sid[subnet['sid']]['dhcp']:
                dhcp_information['subnets_with_dhcp_disabled'] += 1
                continue

            # mostRecentDHCP can have three values
            # 1. ''    -> Empty string. Assumed to be similar to never
            # 2. Date  -> Date of last DHCP packet seen
            # 3. Never -> Never seen DHCP or not tracking
            #               - Because DHCP tracking is disabled (covered in statement above)
            #               - Because no client devices are inside the subnet (covered in statement below)
            if (subnet['mostRecentDHCP'] == 'Never') and subnet['clientDevices'] == 0:
                dhcp_information['subnets_without_clients'] += 1
                continue

            # dhcpQuality is reported for subnets that have seen DHCP
            # If dhcpQuality is missing, we have a subnet with
            if 'dhcpQuality' in subnet:
                dhcp_information['subnets_tracking_dhcp'] += 1
                dhcp_information['total_dhcp_quality'] += int(subnet['dhcpQuality'])
            else:
                dhcp_information['subnets_failing_dhcp'] += 1

        dhcp_information['average_dhcp_quality'] = \
            round(dhcp_information['total_dhcp_quality'] /
                  dhcp_information['subnets_tracking_dhcp'])

        dhcp_statistics.append(dhcp_information)

    return dhcp_statistics


def get_summary(api):
    # Not finished yet. Need to perform subnet summary
    # Count of total subnets seen (per instance/per probe)
    # Subnet
    """
    Provide a summary of subnets seen by Darktrace

    :param api: A valid and active authenticated session with the DarkTrace API
    :return: Dictionary of subnet information per instance
    """
    subnets = api.get('/subnets')
    return subnets


def convert_to_subnets_by_sid(subnets):
    """
    Function to convert Darktrace subnets dict into a dict with key SID. This is handy
    for lookups based on SID.

    We could do api.get('/subnets?sid=<sid>') however this would result in an insane
    amount of requests to DT.
    :param subnets: dict
    :return: dict
    """
    subnets_by_sid = {}
    for subnet in subnets:
        subnets_by_sid[subnet.pop('sid')] = subnet
    return subnets_by_sid

"""Functions used by the Click system subcommand"""
import re
from dtctl.utils.timeutils import fmttime, prstime


def get_summary_statistics(api, **kwargs):
    """
    Retrieves a summary of statistics as collected by Darktrace.

    :param api: Darktrace API object with initialized config values
    :return: Dictionary that contains summary statistics
    """
    # {
    #   "usercredentialcount": 167887,
    #   "bandwidth": [
    #     {
    #       "timems": 1554717600000,
    #       "time": "2019-04-08 10:00:00",
    #       "kb": 70457332415
    #     },
    #     {
    #       "timems": 1554804000000,
    #       "time": "2019-04-09 10:00:00",
    #       "kb": 69610198833
    #     }
    #   ],
    #   "subnets": 5399,
    #   "patterns": 98607390,
    #   "devicecount": {
    #     "total": 240176,
    #     "unknown": 38853,
    #     "totalServer": 42203,
    #     "totalClient": 121229,
    #     "totalOther": 76744
    #   }
    # }
    return api.get('/summarystatistics', **kwargs)


def get_status(api, **kwargs):
    """
    System status of master instances and connected probes

    :param api: Darktrace API object with initialized config values
    :return: Dictionary that contains status values
    """
    return api.get('/status', **kwargs)


def get_usage(api, **kwargs):
    """
    Resource usage of master instances and connected probes

    :param api: Darktrace API object with initialized config values
    :return: Dictionary that contains parsed resource information
    """
    status_dict = api.get('/status', **kwargs)
    usage_dict = {}

    for instance_key, instance_values in status_dict['instances'].items():
        usage_dict[instance_key] = {}
        usage_dict[instance_key]['cpu'] = instance_values['cpu']
        usage_dict[instance_key]['dtqueue'] = instance_values['darkflowQueue']
        usage_dict[instance_key]['memused'] = instance_values['memoryUsed']
        usage_dict[instance_key]['bandwidth'] = instance_values['bandwidthCurrent']
        usage_dict[instance_key]['connectionsPerMinuteCurrent'] = instance_values['connectionsPerMinuteCurrent']
        usage_dict[instance_key]['label'] = instance_values['label']
        usage_dict[instance_key]['probes'] = {}

        for probe_key, probe_values in instance_values['probes'].items():
            usage_dict[instance_key]['probes'][probe_key] = {}
            usage_dict[instance_key]['probes'][probe_key]['label'] = probe_values['label']
            usage_dict[instance_key]['probes'][probe_key]['bandwidthCurrent'] = probe_values['bandwidthCurrent']
            usage_dict[instance_key]['probes'][probe_key]['memoryUsed'] = probe_values['memoryUsed']
            usage_dict[instance_key]['probes'][probe_key]['connectionsPerMinuteCurrent'] = \
                probe_values['connectionsPerMinuteCurrent']
            usage_dict[instance_key]['probes'][probe_key]['cpu'] = probe_values['cpu']

    return usage_dict


def get_tags(api, **kwargs):
    """
    List of tags currently configured within Darktrace

    :param api: Darktrace API object with initialized config values
    :return: Dictionary that contains all tags
    """
    return api.get('/tags', **kwargs)


def get_info(api, **kwargs):
    """
    List Darktrace systeminfo such as version, build, uptime, etc

    :param api: Darktrace API object with initialized config values
    :return: Dictionary that contains system information
    """
    return api.get('/time', **kwargs)


def get_instances(api, **kwargs):
    """
    Get Darktrace master instances, their labels and id numbers.
    id numbers are useful because they are used in breach ids
    Breach ids starts with instance id and than a unique range of numbers.

    A label can be structured in multiple free-format ways. If there is a
    '-' in the label, we assume that the first part is a 'location' or 'region'

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param kwargs: All arguements needing to be passed to the API call
    :type kwargs: Dict
    :return: Darktrace master instances with their labels and ids
    :rtype: Dict
    """
    status = api.get('/status', **kwargs)
    instances = {}

    for instance_name, values in status['instances'].items():
        instances[instance_name] = {'id': values['id'], 'label': values['label']}

        if '-' in values['label']:
            instances[instance_name]['location'] = values['label'].split('-')[0].strip()
    return instances


def get_auditlog(api, **kwargs):
    """
    View account activity log

    :param api: Darktrace API object with initialized config values
    :param **kwargs: Any url parameter needed to pass to the API.
                     For autilog: offset, limit
    :return: Dictionary that contains system information
    """
    # accountactivity?offset=0&limit=30
    return api.get('/accountactivity', **kwargs)


def get_packet_loss(api, start_date, end_date):
    """
    View packet loss information based on Darktrace's system::packet_loss model

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param start_date: DateTime object that represents the start time for which breaches to report on
    :type start_date: DateTime
    :param end_date: DateTime object that represents the end time for which breaches to report on
    :type end_date: DateTime
    :return:
    :rtype:
    """
    start_date = fmttime(start_date) if start_date else None
    end_date = fmttime(end_date) if end_date else None

    models = api.get('/models')
    packet_loss_model = None

    for model in models:
        if model['name'] != 'System::Packet Loss':
            continue
        packet_loss_model = model

    packet_loss_breaches = api.get('/modelbreaches', pid=packet_loss_model['pid'],
                                   starttime=start_date, endtime=end_date)

    return extract_packet_loss_information(packet_loss_breaches)


def extract_packet_loss_information(packet_loss_breaches):
    """
    Extract packet loss information from trigger values in breaches

    :param packet_loss_breaches: Breaches from the packet loss model
    :type packet_loss_breaches: List
    :return: Packet loss statistics per system
    :rtype: Dict
    """
    result = {}

    host_regex = r'Host (.+?):'
    valid_ip_regex = r'\d+\.\d+\.\d+\.\d+$'
    packet_loss_regex = r'rate above ([0-9]+\.[0-9]+)'
    worker_drop_regex = r'worker drop rate: ([0-9]+\.[0-9]+)'

    for breach in packet_loss_breaches:
        for triggered_component in breach['triggeredComponents']:
            for triggered_filter in triggered_component['triggeredFilters']:
                if triggered_filter['comparatorType'] == 'display':
                    continue

                value = triggered_filter['trigger']['value']
                packet_loss_percentage = re.search(packet_loss_regex, value)[1]
                worker_drop_percentage = re.search(worker_drop_regex, value)[1]
                host = re.search(host_regex, value)[1]
                ip_address = re.search(valid_ip_regex, host)[0]

                info_dict = {'date': '{0}'.format(prstime(triggered_component['time'])),
                             'packet_loss': packet_loss_percentage,
                             'worker_drop_rate': worker_drop_percentage}

                if ip_address in result:
                    result[ip_address].append(info_dict)
                else:
                    result[ip_address] = [info_dict]
    return result

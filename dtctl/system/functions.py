"""Functions used by the Click system subcommand"""
import re
from dtctl.utils.timeutils import fmttime, prstime, utc_now_timestamp


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
    usage_list = []

    for _instance_key, instance_values in status_dict['instances'].items():
        info = {
            'system': instance_values['hostname'],
            # 'ip': instance_key,  # instance_key is not an IP for masters. Replace when 'ip' key is made available
            'type': 'master',
            'timestamp': utc_now_timestamp(),
            'cpu': instance_values['cpu'],
            'dtqueue': instance_values['darkflowQueue'],
            'memused': instance_values['memoryUsed'],
            'bandwidth': instance_values['bandwidthCurrent'],
            'connectionsPerMinuteCurrent': instance_values['connectionsPerMinuteCurrent'],
            'label': instance_values['label']
        }

        usage_list.append(info)

        for probe_key, probe_values in instance_values['probes'].items():
            # In case a probe has errors, we skip from calculating usage
            try:
                if probe_values['error']:
                    continue
            except KeyError:
                pass

            info = {
                'system': probe_values['hostname'],
                'ip': probe_key,
                'type': 'probe',
                'timestamp': utc_now_timestamp(),
                'label': probe_values['label'],
                'bandwidth': probe_values['bandwidthCurrent'],
                'memused': probe_values['memoryUsed'],
                'connectionsPerMinuteCurrent': probe_values['connectionsPerMinuteCurrent'],
                'cpu': probe_values['cpu']
            }

            usage_list.append(info)

    return usage_list


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


def get_instances(api, show_probes, **kwargs):
    """
    Get Darktrace master instances, their labels and id numbers.
    Id numbers are useful because they are used in breach ids.
    Breach ids starts with instance id followed by a unique range of numbers.

    A label can be structured in multiple free-format ways. If there is a
    '-' in the label, we assume that the first part is a 'location' or 'region'

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param show_probes: To include probe information in output
    :type show_probes: Bool
    :param kwargs: All arguments needing to be passed to the API call
    :type kwargs: Dict
    :return: Darktrace master instances with their labels and ids
    :rtype: Dict
    """
    status = api.get('/status', **kwargs)
    instances = {}

    for instance_name, values in status['instances'].items():
        instances[instance_name] = {'id': values['id'], 'label': values['label'], 'version': values['version']}

        if '-' in values['label']:
            instances[instance_name]['location'] = values['label'].split('-')[0].strip()

        if show_probes:
            for probe, probe_values in values['probes'].items():
                # In case a probe has errors, we skip further processing
                try:
                    if probe_values['error']:
                        continue
                except KeyError:
                    pass

                probe_info = {
                    'id': probe_values['id'], 'ip': probe, 'label': probe_values['label'],
                    'version': probe_values['version']
                }

                if '-' in probe_values['label']:
                    probe_info['location'] = probe_values['label'].split('-')[0].strip()

                if 'probes' not in instances[instance_name]:
                    instances[instance_name]['probes'] = [probe_info]
                else:
                    instances[instance_name]['probes'].append(probe_info)

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
    :return: JSON objects containing packet-loss information
    :rtype: List
    """
    start_date = fmttime(start_date) if start_date else None
    end_date = fmttime(end_date) if end_date else None

    models = api.get('/models')
    packet_loss_model = None

    # Unsure if for all Darktrace installations the packet loss model has the same ID
    # therefore we loop through all models
    for model in models:
        if model['name'] == 'System::Packet Loss':
            packet_loss_model = model
            break

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
    result = []

    host_regex = r'Host (.+?):'
    valid_ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
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
                hostname = '-'.join(host.split('-')[0:-1])
                ip_address = re.search(valid_ip_regex, host)[0]

                info_dict = {
                    'system': hostname,
                    'ip': ip_address if ip_address else host,
                    'timestamp': '{0}'.format(prstime(triggered_component['time'], True)),
                    'packet_loss': float(packet_loss_percentage),
                    'worker_drop_rate': float(worker_drop_percentage)
                }

                result.append(info_dict)
    return result


def get_system_issues(api, start_date, end_date):
    """
    View Darktrace system issues by querying the system::issue model

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param start_date: DateTime object that represents the start time for which breaches to report on
    :type start_date: DateTime
    :param end_date: DateTime object that represents the end time for which breaches to report on
    :type end_date: DateTime
    :return: JSON objects containing packet-loss information
    :rtype: List
    """
    start_date = fmttime(start_date) if start_date else None
    end_date = fmttime(end_date) if end_date else None

    status = api.get('/status')
    models = api.get('/models')
    system_issue_model = None

    # Unsure if for all Darktrace installations the packet loss model has the same ID
    # therefore we loop through all models
    for model in models:
        if model['name'] == 'System::System':
            system_issue_model = model
            break

    system_issue_breaches = api.get('/modelbreaches', pid=system_issue_model['pid'],
                                    starttime=start_date, endtime=end_date)

    return extract_system_issue_information(system_issue_breaches, status)


def extract_system_issue_information(system_issue_breaches, status):
    """
    Extract system issue information from trigger values in breaches

    :param system_issue_breaches: Breaches from the system model
    :type system_issue_breaches: List
    :param status: Darktrace status information
    :type status: Dict
    :return: Identified system issues
    :rtype: Dict
    """
    result = []

    # valid_ip_regex = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

    try:
        unified_view_hostname = status['hostname']
    except KeyError:
        unified_view_hostname = 'unknown'

    for breach in system_issue_breaches:
        for triggered_component in breach['triggeredComponents']:
            for triggered_filter in triggered_component['triggeredFilters']:
                if triggered_filter['comparatorType'] == 'display' or triggered_filter['filterType'] != 'Event details':
                    continue

                value = triggered_filter['trigger']['value']
                # Currently not using this as it is most likely the source
                # of a faulty probe or master and not the source of the
                # originating device
                # ip_address = re.search(valid_ip_regex, value)[0]

                info_dict = {
                    'system': unified_view_hostname,
                    'timestamp': '{0}'.format(prstime(triggered_component['time'], True)),
                    'message': value
                }

                result.append(info_dict)
                break

    return result

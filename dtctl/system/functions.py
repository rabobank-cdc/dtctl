"""Functions used by the Click system subcommand"""


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

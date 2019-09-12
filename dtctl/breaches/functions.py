# pylint: disable=C0325
"""Functions used by the Click breaches subcommand"""

import pandas as pd
from pandas.io.json import json_normalize
from dtctl.utils.timeutils import fmttime, prstime
from dtctl.utils.parsing import convert_series
from dtctl.utils.reporting import format_report, device_info


def get_breaches(api, acknowledged, tags, minimal, minscore, start_date, end_date):
    """
    Function to get breaches based on filters and flags

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param acknowledged: Value of acknowledged flag
    :type acknowledged: Boolean
    :param tags: Tags to filter on
    :type tags: List
    :param minimal: Value of minimal flag
    :type minimal: Boolean
    :param minscore: Minimum score of breaches to filter on
    :type minscore: Float
    :param start_date:
    :type start_date: DateTime
    :param end_date:
    :type end_date: DateTime
    :return: Filtered breaches
    :rtype: List
    """
    start_date = fmttime(start_date) if start_date else None
    end_date = fmttime(end_date) if end_date else None

    str_acknowledged = str(acknowledged).lower() if acknowledged else 'false'
    str_minimal = str(minimal).lower() if minimal else 'false'

    breaches = api.get('/modelbreaches', starttime=start_date, endtime=end_date, includeacknowledged=str_acknowledged,
                       minimal=str_minimal, historicmodelonly='true', includebreachurl='true', minscore=minscore)

    if acknowledged:
        breaches = filter_acknowledged_breaches(breaches)

    if tags:
        breaches = filter_breaches_by_tag(breaches, tags)

    return breaches


def all_breaches(api, start_date, end_date):
    """
    Get all model breaches

    :param api: Darktrace API object with initialized config values
    :param start_date: DateTime object that represents the start time for which breaches to report on
    :param end_date: DateTime object that represents the end time for which breaches to report on
    :return: List of all breaches
    """
    start_date = fmttime(start_date) if start_date else None
    end_date = fmttime(end_date) if end_date else None

    breaches = api.get('/modelbreaches', starttime=start_date, endtime=end_date, includeacknowledged='true',
                       historicmodelonly='true', minimal='false', includebreachurl='true')
    return breaches


def acknowledged_breaches(api, start_date, end_date):
    """
    Get all acknowledged model breaches

    :param api: Darktrace API object with initialized config values
    :param start_date: DateTime object that represents the start time for which breaches to report on
    :param end_date: DateTime object that represents the end time for which breaches to report on
    :return: List with acknowledged breaches
    """
    breaches = all_breaches(api, start_date, end_date)
    return filter_acknowledged_breaches(breaches)


def report_breaches(program_state, arg, start_date, end_date, output_file, template, output_format):
    """
    Report on model breaches

    :param program_state: ProgramState object
    :param arg: Which type of report to create. Acknowledged or commented
    :param start_date: DateTime object that represents the start time for which breaches to report on
    :param end_date: DateTime object that represents the end time for which breaches to report on
    :param output_file: Filename in String where the report should be saved to
    :param template: Filename in String of template where to append new data to
    :param output_format: String that specifies output format
    :return: None
    """
    start_date = fmttime(start_date) if start_date else None
    end_date = fmttime(end_date) if end_date else None

    report_functions = {
        'commented': report_commented_breaches,
        'acknowledged': report_acknowledged_breaches,
        'brief': report_breaches_brief
    }

    report_functions[arg](program_state, start_date, end_date, output_file, template, output_format)


def report_commented_breaches(program_state, start_date, end_date, output_file, template, output_format):
    """
    Create a report that holds all model breaches for which
    comments have been entered.

    :param program_state: ProgramState object
    :param start_date: DateTime object that represents the start time for which breaches to report on
    :param end_date: DateTime object that represents the end time for which breaches to report on
    :param output_file: Filename in String where the report should be saved to
    :param template: Filename in String of template where to append new data to
    :param output_format: String that specifies output format
    :return: None
    """
    comments_json = program_state.api.get('/mbcomments', starttime=start_date, endtime=end_date)

    comments = pd.DataFrame(comments_json).sort_values('time', ascending=True)

    comments['comment'] = comments[['username', 'message']].apply(': '.join, axis=1)

    grouped = comments.groupby('pbid')
    joined = grouped.comment.apply('\n'.join)
    unique = grouped.first()
    unique['model_name'] = unique.name
    unique['comments'] = joined
    unique['first_comment_by'] = unique['username']

    breaches_json = []
    total = len(unique.index)
    for count, pbid in enumerate(unique.index):
        breaches_json.append(program_state.api.get('/modelbreaches', pbid=pbid, historicmodelonly=True))
        count += 1
        print(f'{count} out of {total} breaches ({round((count / total) * 100)}%) done')

    breaches = pd.DataFrame([x for x in breaches_json if not x == []])
    breaches.index = breaches.pbid

    breaches['breach_time'] = breaches['time'].map(prstime)
    del(breaches['time'])
    breaches['device_id'] = breaches.triggeredComponents.map(lambda x: device_info(x, 'did'))
    breaches['mac_address'] = breaches.triggeredComponents.map(lambda x: device_info(x, 'macaddress'))
    breaches['ip_address'] = breaches.triggeredComponents.map(lambda x: device_info(x, 'ip'))
    breaches['hostname'] = breaches.triggeredComponents.map(lambda x: device_info(x, 'hostname'))
    breaches['type'] = breaches.triggeredComponents.map(lambda x: device_info(x, 'typelabel'))
    breaches['link'] = breaches['pbid'].map(lambda x: '{0}/#modelbreach/{1}'.format(program_state.config['host'],
                                                                                    str(x)))

    merged = unique.join(breaches)

    columns = ['model_name', 'breach_time', 'device_id', 'mac_address', 'ip_address',
               'hostname', 'type', 'first_comment_by', 'comments', 'link']

    format_report(merged[columns].sort_values('breach_time', ascending=True), output_file, template, output_format)


def report_acknowledged_breaches(program_state, start_date, end_date, output_file, template, output_format):
    """
    Create a report that holds all model breaches that have been acknowledged

    :param program_state: ProgramState object
    :param start_date: DateTime object that represents the start time for which breaches to report on
    :param end_date: DateTime object that represents the end time for which breaches to report on
    :param output_file: Filename in String where the report should be saved to
    :param template: Filename of template file to write data to. Data is appended to sheet 'RawData' and/or
                    appended to the table 'RawDataTable'
    :param output_format: String that specifies output format
    :return: None
    """
    instances_by_id = get_instances_region(program_state.api)

    breaches = acknowledged_breaches(program_state.api, start_date, end_date)
    breaches_df = json_normalize(breaches)
    breaches_df.index = breaches_df['pbid']
    breaches_df['breach_time'] = breaches_df['time'].map(prstime)
    breaches_df['acknowledged_time'] = breaches_df['acknowledged.time'].map(prstime)
    breaches_df['comment'] = breaches_df['pbid'].map(lambda x: get_comments(program_state.api, x))
    breaches_df['tags'] = breaches_df['model.tags'].map(convert_series)
    breaches_df['device_id'] = breaches_df.triggeredComponents.map(lambda x: device_info(x, 'did'))
    breaches_df['mac_address'] = breaches_df.triggeredComponents.map(lambda x: device_info(x, 'macaddress'))
    breaches_df['ip_address'] = breaches_df.triggeredComponents.map(lambda x: device_info(x, 'ip'))
    breaches_df['hostname'] = breaches_df.triggeredComponents.map(lambda x: device_info(x, 'hostname'))
    breaches_df['type'] = breaches_df.triggeredComponents.map(lambda x: device_info(x, 'typelabel'))
    breaches_df['destination'] = breaches_df.triggeredComponents.map(get_dest_hostname_or_ip)
    breaches_df['region'] = breaches_df['pbid'].map(lambda x: instances_by_id[int(str(x).strip('-')[0])]['region'])
    breaches_df['link'] = breaches_df['pbid'].map(lambda x: '{0}/#modelbreach/{1}'.format(program_state.config['host'],
                                                                                          str(x)))

    rename_mapping = {'model.name': 'model_name', 'commentCount': 'comments',
                      'acknowledged.username': 'acknowledged_by'}
    breaches_df.rename(columns=rename_mapping, inplace=True)

    columns = ['model_name', 'breach_time', 'device_id', 'mac_address', 'ip_address', 'hostname', 'type',
               'destination', 'acknowledged_by', 'comment', 'comments', 'acknowledged_time', 'score', 'tags',
               'link', 'region']

    format_report(breaches_df[columns].sort_values('breach_time', ascending=True), output_file, template, output_format)


def report_breaches_brief(program_state, start_date, end_date, output_file, template, output_format):
    """
    Brief report of breaches that excludes comments and detailed meta data

    :param program_state: ProgramState object
    :param start_date: DateTime object that represents the start time for which breaches to report on
    :param end_date: DateTime object that represents the end time for which breaches to report on
    :param output_file: Filename in String where the report should be saved to
    :param output_file: Filename in String where the report should be saved to
    :param template: Filename of template file to write data to. Data in sheet 'RawData' is overwritten
    :param output_format: String that specifies output format
    :return: None
    """
    # Get status information in order to get instance ID and label (for region)
    instances_by_id = get_instances_region(program_state.api)
    breaches = all_breaches(program_state.api, start_date, end_date)
    breaches_df = json_normalize(breaches)
    breaches_df.index = breaches_df['pbid']
    breaches_df['region'] = breaches_df['pbid'].map(lambda x: instances_by_id[int(str(x).strip('-')[0])]['region'])
    breaches_df['hostname'] = breaches_df.triggeredComponents.map(get_hostname_or_ip)
    breaches_df['category'] = breaches_df['model.name'].map(lambda x: x.split('::')[0])
    breaches_df['enhanced'] = breaches_df['model.tags'].map(has_enhanced_tag)
    breaches_df['acknowledged'] = breaches_df['acknowledged'].map(lambda x: 1 if x else 0)
    breaches_df['tags'] = breaches_df['model.tags'].map(convert_series)
    breaches_df['time'] = breaches_df['time'].map(prstime)
    rename_mapping = {'model.name': 'model_name'}
    breaches_df.rename(columns=rename_mapping, inplace=True)

    columns = ['region', 'hostname', 'model_name', 'score', 'category', 'enhanced', 'acknowledged', 'tags', 'time']

    format_report(breaches_df[columns], output_file, template, output_format)


def has_enhanced_tag(tags):
    """
    Simple function to check if 'Enhanced' tag is in a list of tags
    returns integer instead of boolean for Excel count and sum funtionality

    :return: int: 1 if contains Enhanced, 0 if not
    """
    if isinstance(tags, list):
        if tags:
            for tag in tags:
                if 'enhanced' in tag.lower():
                    return 1
        return 0
    return 0


def get_dest_hostname_or_ip(components):
    """
    Retrieve destination for a breach from its triggeredComponents
    A destination can be an IP address, hostname or an event message.

    :param components: Array of 'triggeredComponents'
    :return: str: Destination
    """
    # These are the filter_types that are most often used to
    # display the "to" field in the Darktrace UI
    filter_types = ['Connection hostname', 'Destination IP']
    destination = ''
    for record in components:
        if 'triggeredFilters' not in record:
            continue

        for trigger in record['triggeredFilters']:
            if trigger['filterType'] in filter_types and trigger['comparatorType'] == 'display':
                if trigger['trigger']['value']:  # Could be empty string in some hostname case
                    destination = trigger['trigger']['value']

            # Last resort is to take the message
            if not destination and trigger['filterType'] == 'Message' and trigger['comparatorType'] == 'display':
                destination = trigger['trigger']['value']

    return destination


def get_instances_region(api):
    """
    Simple function to get a dict with key instance_id and value labels

    :param api: Darktrace API object with initialized config values
    :return: dict: Containing dictionary with instance ids and their labels
    """
    status = api.get('/status')
    instances = {}
    for _, values in status['instances'].items():
        instances[values['id']] = {'label': values['label']}
        if '-' in values['label']:
            instances[values['id']]['region'] = values['label'].split('-')[0].strip()
    return instances


def get_hostname_or_ip(components):
    """
    Simple function to get a dict with key instance_id and value labels

    :param components: Array of 'triggeredComponents'
    :return: str: either Hostname or IP address
    """
    for record in components:
        if 'device' not in record:
            continue

        if 'hostname' in record['device']:
            if record['device']['hostname']:
                return record['device']['hostname']

        if 'ip' in record['device']:
            if record['device']['ip']:
                return record['device']['ip']

    return 'Unknown'


def get_comments(api, pbid):
    """
    Simple function to retrieve compiled breach comments for a given breach id.

    :param api: Darktrace API object with initialized config values
    :param pbid: Model breach id
    :return: string: Compiled message containing all user comments (username:comment)
    """
    comments = api.get('/mbcomments', pbid=pbid)
    message = ''

    for comment in comments:
        message += '{0}:{1}\n'.format(comment['username'], comment['message'])
    return message


def filter_acknowledged_breaches(breaches):
    """
    Function to filter out acknowledged breaches

    :param breaches: Breaches to filter
    :type breaches: List
    :return: Acknowledged breaches
    :rtype: List
    """
    acknowledged_breaches_list = []
    for breach in breaches:
        if breach['acknowledged']:
            acknowledged_breaches_list.append(breach)
    return acknowledged_breaches_list


def filter_breaches_by_tag(breaches, tags_to_filter):
    """
    Function to filter breaches based on tags

    :param breaches: Breaches to filter
    :type breaches: List
    :param tags_to_filter: Tags to filter on
    :type tags_to_filter: List
    :return: Filtered breaches
    :rtype: List
    """
    filtered_breaches = []

    for breach in breaches:
        for tag in breach['model']['tags']:
            if tag in tags_to_filter:
                filtered_breaches.append(breach)
    return filtered_breaches

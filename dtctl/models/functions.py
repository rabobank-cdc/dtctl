# pylint: disable=C0121
# pylint: disable=E1135
"""Functions used by the Click models subcommand"""
import os
import fnmatch
import datetime as dt
import pandas as pd
from pandas.io.json import json_normalize
import click
from dtctl.utils.timeutils import fmttime


def select_models_by_key_values(api, key_values):
    """
    View models filtered by key value. Currently does not support nesting
    and as such only supports top-level key-value pairs of models

    :param api: A valid and active authenticated session with the Darktrace API
    :type api: Api
    :param key_values: Key value pairs to filter on
    :type key_values: Dict
    :return: Selected models
    :rtype: List
    """
    models = api.get('/models')
    selected_models = []
    for model in models:
        for key, value in key_values.items():
            if key not in model:
                continue
            if str(model[key]).lower() == value.lower():
                selected_models.append(model)
    return selected_models


def get_deleted_models(api, enhanced_only, active_only, infile, **_):
    """
    Compare list of models against Darktrace models. Models in the supplied list
    that are NOT in the models retrieved from Darktrace are considered deleted.

    :param api: A valid and active authenticated session with the Darktrace API
    :type api: Api
    :param enhanced_only: Flag for getting only models with tag '*enhanced*'
    :type enhanced_only: Boolean
    :param active_only: Flag for getting only active models
    :type active_only: Boolean
    :param infile: Path to file with model names on each line
    :type infile: String
    :return: Models that are NOT in the supplied list
    :rtype: Dict
    """
    models = api.get('/models')
    selected_models = filter_models_by_flags(models, enhanced_only, active_only)
    input_models = get_models_from_infile(infile)
    selected_models = [model['name'] for model in selected_models]

    return list(set(input_models) - set(selected_models))


def get_new_models(api, enhanced_only, active_only, infile, **_):
    """
    Compare list of models against Darktrace models filtered by a date range.
    Models retrieved from Darktrace that are NOT in the supplied list are returned

    :param api: A valid and active authenticated session with the Darktrace API
    :type api: Api
    :param enhanced_only: Flag for getting only models with tag '*enhanced*'
    :type enhanced_only: Boolean
    :param active_only: Flag for getting only active models
    :type active_only: Boolean
    :param infile: Path to file with model names on each line
    :type infile: String
    :return: Models that are NOT in the supplied list
    :rtype: Dict
    """
    models = api.get('/models')
    selected_models = filter_models_by_flags(models, enhanced_only, active_only)
    input_models = get_models_from_infile(infile)
    selected_models = [model['name'] for model in selected_models]

    return list(set(selected_models) - set(input_models))


def get_models_with_changes(api, enhanced_only, active_only, infile, **kwargs):
    """
    Compare list of models against Darktrace models filtered by a date range.
    Models in the supplied list, also in the models filtered by date range are returned

    :param api: A valid and active authenticated session with the Darktrace API
    :type api: Api
    :param enhanced_only: Flag for getting only models with tag '*enhanced*'
    :type enhanced_only: Boolean
    :param active_only: Flag for getting only active models
    :type active_only: Boolean
    :param infile: Path to file with model names on each line
    :type infile: String
    :param kwargs: Additional parameters for get_models_by_date_range
    :type kwargs: Dict
    :return: Models from the supplied lists that have been modified within date range
    :rtype: Dict
    """
    models = api.get('/models')
    selected_models = filter_models_by_flags(models, enhanced_only, active_only)
    selected_models = get_models_by_date_range(selected_models, **kwargs)
    input_models = get_models_from_infile(infile)
    selected_models = [model['name'] for model in selected_models]

    return list(set(selected_models) & set(input_models))


def get_models_from_infile(infile):
    """
    Retrieve model names from input file

    :param infile: Path to input file with models to compare
    :type infile: String
    :return: Difference between supplied models and models in input file
    :rtype: Dict
    """
    if not os.path.exists(infile):
        raise click.UsageError('File "{0}" does not exist'.format(infile))

    input_models = []
    with open(infile) as infile_fd:
        for line in infile_fd.readlines():
            input_models.append(line.strip())

    return input_models


def get_models_by_date_range(models, **kwargs):
    """
    Filter models by date range

    :param models: The models to filter
    :type models: Dict
    :param kwargs: Additional key value pairs. Must contain start_date and end_date
    :type kwargs: Dict
    :return: Filtered models
    :rtype: List
    """
    if 'start_date' not in kwargs:
        raise TypeError

    if 'end_date' not in kwargs:
        raise TypeError

    start_date = kwargs['start_date']
    end_date = kwargs['end_date']

    filtered_models = []
    for model in models:
        model_datetime = dt.datetime.strptime(model['modified'], '%Y-%m-%d %H:%M:%S')
        if start_date <= model_datetime <= end_date:
            filtered_models.append(model)
    return filtered_models


def get_models(api, enhanced_only, active_only, with_components, filter_tag):
    """
    Generic function for listing models. If the enhanced_only flag is provided
    only list models that have that tag

    :param api: A valid and active authenticated session with the Darktrace API
    :type api: Api
    :param enhanced_only: Only filter models with *enhanced* flag
    :type enhanced_only: Boolean
    :param active_only: Only filter models that are active
    :type active_only: Boolean
    :param with_components: Display model components
    :type with_components: Boolean
    :param filter_tag: String that filters listed models based on specified tag
    :return: Dict of models
    """
    models = api.get('/models')
    if with_components:
        models = get_model_components(api, models)

    selected_models = filter_models_by_flags(models, enhanced_only, active_only)

    if filter_tag:
        return get_models_filtered_by_tag(filter_tag, selected_models)

    return selected_models


def get_model_components(api, models):
    """
    Get components for each model

    :param api: A valid and active authenticated session with the Darktrace API
    :type api: Api
    :param models: List of models to get components for
    :type models: List
    :return: Models including their components list
    :rtype: List
    """
    components = api.get('/components')
    models_to_return = []
    for model in models:
        for component in model['logic']['data']:
            if isinstance(component, dict):
                cid = component['cid']
            else:
                cid = component

            components_for_model = [x for x in components if x['cid'] == cid]

            if 'components' in model:
                model['components'].extend(components_for_model)
            else:
                model['components'] = components_for_model

        models_to_return.append(model)
    return models_to_return


def get_enhanced_only_models(active_only, models):
    """
    Function for listing enhanced models. If the active_only flag is provided
    only list models that have *enhanced* tag and are active

    :param active_only: Boolean for listing only enhanced models that are active
    :param models: Dict of models to filter on enhanced (and active_only)
    :return: Dict of filtered models
    """
    enhanced_models = []
    for model in models:
        if active_only:
            if not model['active']:
                continue

        try:
            for tag in model['tags']:
                if 'enhanced' in tag.lower():
                    enhanced_models.append(model)
        except KeyError:
            pass
    return enhanced_models


def get_active_only_models(active_only, filter_tag, models):
    """
    Function for listing active models. If the filter_tag is provided
    only list models that have a specific tag

    :param active_only: Boolean for listing only enhanced models that are active
    :param filter_tag: Dict of models to filter on tag (and active_only)
    :param models: Dict of models
    :return: Dict of filtered models
    """
    active_models = []
    for model in models:
        if active_only:
            if not model['active']:
                continue

        if filter_tag:
            try:
                for tag in model['tags']:
                    if filter_tag.lower() in tag.lower():
                        active_models.append(model)
            except KeyError:
                pass
        else:
            active_models.append(model)
    return active_models


def get_models_filtered_by_tag(filter_tag, models):
    """
    Function for listing all models filtered by tag

    :param filter_tag: Dict of models to filter on tag
    :param models: Dict of models
    :return: Dict of filtered models
    """
    filtered_models = []
    for model in models:
        try:
            for tag in model['tags']:
                if filter_tag.lower() in tag.lower():
                    filtered_models.append(model)
        except KeyError:
            pass
    return filtered_models


def get_autoupdatable(api, **kwargs):
    """
    Function for listing all models that have autoupdatable set to yes

    :param api: A valid and active authenticated session with the DarkTrace API
    :return: None
    """
    models = api.get('/models', **kwargs)
    autoupdatable_models = []

    for model in models:
        if model['autoUpdatable'] and model['autoUpdate']:
            autoupdatable_models.append(model['name'])
    return autoupdatable_models


def get_pending_updates(api, **kwargs):
    """
    Function for listing all models with pending updates

    Background:
    Models for which the first history object is inactive have an update pending.
    Note that the history list is not guaranteed to be ordered when serialized from
    JSON into a python dict

    :param api: A valid and active authenticated session with the DarkTrace API
    :return: None
    """
    models = api.get('/models', **kwargs)
    models_with_updates = []
    for model in models:
        history_sorted = sorted(model['history'], key=lambda k: k['modified'], reverse=True)
        if not history_sorted[0]['active']:
            models_with_updates.append(model)
    return models_with_updates


# This is potentially already functionality in Darktrace itself. I.e. models with changes are not updated automagically
def get_updatable(api, **kwargs):
    """
    Function for listing all models that can be safely upgraded without losing
    custom modifications.

    Background:
    Models being upgraded/updated lose all previous modification. Hence if the last
    history object was applied by a system user, we can safely update ## Is this true?

    :param api: A valid and active authenticated session with the DarkTrace API
    :return: None
    """
    models = api.get('/models', **kwargs)
    models_updatable = []

    for model in models:
        history_sorted = sorted(model['history'], key=lambda k: k['modified'], reverse=True)
        if not history_sorted[0]['active']:
            if history_sorted[1]['by'] not in ['darktrace', 'System', 'nobody']:
                models_updatable.append(model['name'])
    return models_updatable


def filter_models_by_flags(models, enhanced_only, active_only):
    """
    Filter models based on enhanced tags and activeness

    :param models: Models to filter
    :type models: Dict
    :param enhanced_only: Only filter models with *enhanced* flag
    :type enhanced_only: Boolean
    :param active_only: Only filter models that are active
    :type active_only: Boolean
    :return: Filtered models
    :rtype: Dict
    """
    if enhanced_only:
        return get_enhanced_only_models(active_only, models)

    if active_only:
        return get_active_only_models(active_only, None, models)

    return models


def report_models(api, **kwargs):
    """
    Function for creating an excel report for DarkTrace models.

    :param api: A valid and active authenticated session with the DarkTrace API
    :return: None
    """
    output_file = kwargs['outfile']
    active_only = kwargs['active_only']

    models = pd.DataFrame(api.get('/models'))

    if active_only:
        models = models[models.active == True]
    models['idx'] = models.index

    history_list = []
    for _, row in models[['idx', 'history']].iterrows():
        idx, events = row
        for event in events:
            event['idx'] = idx
            history_list.append(event)
    history = pd.DataFrame(history_list)

    models_columns = [x for x in models.columns if x not in history.columns] + ['idx']
    columns = ['pid', 'name', 'active', 'modified', 'created', 'by', 'message', 'description', 'tags', 'phid']

    merged = history.merge(models[models_columns], on='idx')
    merged[columns].sort_values(['pid', 'modified'], ascending=True).to_excel(output_file)


def breach_summary(api, **kwargs):
    """
    Function for listing nr of breaches per model

    :param api: A valid and active authenticated session with the DarkTrace API
    :return: None
    """
    start_date = fmttime(kwargs['start_date']) if kwargs['start_date'] else None
    end_date = fmttime(kwargs['end_date']) if kwargs['end_date'] else None

    breaches = api.get('/modelbreaches', starttime=start_date, endtime=end_date,
                       includeacknowledged='true', historicmodelonly='true', minimal='false')

    breaches_df = json_normalize(breaches)
    breaches_df['acknowledged'] = breaches_df['acknowledged'].map(bool)

    summary_df = pd.DataFrame(columns=['nr_of_breaches', 'nr_of_acknowledged'])

    for name, group in breaches_df.groupby('model.name'):
        nr_of_breaches = len(group)
        nr_of_acknowledged = group[group.acknowledged == True]['acknowledged'].count()

        # DF holds the following structure
        #               nr_of_breaches      nr_of_acknowledged
        # model.name
        summary_df.loc[name] = [nr_of_breaches, nr_of_acknowledged]

    summary_df.to_excel(kwargs['outfile'])


def get_rules(api, list_of_cids):
    """
    Retrieve rules from Darktrace based on a list of cids

    :param api: Valid and authenticated Darktrace API instance
    :type api: Api
    :param list_of_cids: A list of CIDs for which to get rules
    :type list_of_cids: List
    :return: List of components
    :rtype: List
    """
    components = api.get('/components')
    return [x for x in components if x['cid'] in list_of_cids]


def search_models(api, name_query):
    """
    Function to search for models by quering model names

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param name_query: Shell-style search string potentially containing wildcards
    :type name_query: String
    :return: Found devices or tags
    :rtype: List
    """
    if name_query:
        models = api.get('/models')
        qualifying_models = []

        for model in models:
            if fnmatch.fnmatch(model['name'].lower(), name_query.lower()):
                qualifying_models.append(model)

        return qualifying_models
    return None

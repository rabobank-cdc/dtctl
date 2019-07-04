"""Specific functions for model diffing"""
import collections
from dictdiffer import diff
from dtctl.models.functions import get_pending_updates


def get_update_diffs(api):
    """
    Getting differences between model updates

    :param api: A valid and active authenticated session with the DarkTrace API
    :return: A dict with differences of models with pending updates
    """
    model_differences = []

    models_with_updates = get_pending_updates(api)
    # models_with_updates = ['test']
    for model_with_update in models_with_updates:
        history_sorted = sorted(model_with_update['history'], key=lambda k: k['modified'], reverse=True)
        updated_model = history_sorted.pop(0)

        for history in history_sorted:
            if history['active']:
                active_from_history = history

        updated_model_info = api.get('/models/{0}?phid={1}'.format(model_with_update['pid'], updated_model['phid']))
        active_model_info = api.get('/models/{0}?phid={1}'.format(model_with_update['pid'],
                                                                  active_from_history['phid']))
        # import json
        # with open('updated_model.json') as infile:
        #     updated_model_info = json.load(infile)
        #
        # with open('active_model.json') as infile:
        #     active_model_info = json.load(infile)

        merged_differences = {
            'model': updated_model_info['policy']['name'],
            'message': updated_model_info['policy']['message']
        }

        model_components_differences = get_model_component_differences(updated_model_info,
                                                                       active_model_info)

        # This function currently edits the passed objects inline. Keep this in mind if
        # using these objects after this function call.
        model_policy_differences = get_model_policy_differences(updated_model_info['policy'],
                                                                active_model_info['policy'])

        if model_policy_differences:
            merged_differences['policy'] = model_policy_differences

        if model_components_differences:
            # Merge existing differences and model info with component differences
            merged_differences = {**merged_differences, **model_components_differences}

        model_differences.append(merged_differences)

    return model_differences


def get_model_component_differences(updated_model_info, active_model_info):
    """
    Retrieve differences between two model's component sections.

    Note: Obtaining the differences for the "Logic" key is not yet implemented

    :param updated_model_info: The "components" key from the updated model
    :type updated_model_info: Dict
    :param active_model_info: The "Components" key from the active model
    :type active_model_info: Dict
    :return: Differences between components
    :rtype: Dict
    """
    differences = {'components': []}
    component_keys_to_ignore = ('cid', 'chid', 'mlid', 'active', 'filters', 'logic')

    order_of_cids_for_active_model = determine_cid_order(active_model_info['policy']['logic']['data'])
    order_of_cids_for_updated_model = determine_cid_order(updated_model_info['policy']['logic']['data'])

    updated_model_components_sorted = get_components_by_cid(order_of_cids_for_updated_model,
                                                            updated_model_info['components'])
    active_model_components_sorted = get_components_by_cid(order_of_cids_for_active_model,
                                                           active_model_info['components'])

    if len(updated_model_components_sorted) > len(active_model_components_sorted):
        differences['nr_of_new_components'] = len(updated_model_components_sorted) - \
                                              len(active_model_components_sorted)

    if len(updated_model_components_sorted) < len(active_model_components_sorted):
        differences['nr_of_components_removed'] = len(active_model_components_sorted) - \
                                                  len(updated_model_components_sorted)

    # Our initial work will only work if components changed, but none are added or removed
    if len(updated_model_info['components']) != len(active_model_info['components']):
        return differences

    for index, active_component_dict in enumerate(active_model_components_sorted):
        updated_component_dict = updated_model_components_sorted[index]
        differences['components'].insert(0, {})

        filter_differences = get_filter_differences(updated_component_dict['filters'], active_component_dict['filters'])
        if filter_differences:
            differences['components'][0]['filters'] = filter_differences

        # Delete keys _AFTER_ we obtain filter differences
        # because the 'filter' key is also removed before we
        # check for base differences
        for key_to_delete in component_keys_to_ignore:
            updated_component_dict.pop(key_to_delete, None)
            active_component_dict.pop(key_to_delete, None)

        base_differences = [change for change in diff(active_component_dict, updated_component_dict)]

        if base_differences:
            differences['components'][0]['base'] = base_differences

        if not differences['components'][0]:
            del differences['components'][0]  # No need to report if no differences are present

    return differences


def get_components_by_cid(cid_order, components):
    """
    Inefficient helper function to return a sorted list of components.

    This function exists because Darktrace keeps components order only in the policy -> logic -> data section
    and not in the regular components sections.

    :param cid_order: Order of cids to sort components on
    :type cid_order: List
    :param components: Model components
    :type components: Dict
    :return: Components ordered according to cid_order
    :rtype: List
    """
    ordered_components_list = []
    for cid in cid_order:
        for component in components:
            if cid == component['cid']:
                ordered_components_list.append(component)
    return ordered_components_list


def determine_cid_order(logic_data):
    """
    Simple helper function to extract CID numbers from logic data

    :param logic_data: A model policy's "logic"->"Data" section
    :type logic_data: Dict
    :return: Component IDs
    :rtype: List
    """
    order_list = []
    for item in logic_data:
        if isinstance(item, dict):
            order_list.append(item['cid'])
        else:
            order_list.append(item)
    return order_list


def get_filter_differences(updated_model_component_filters, active_model_component_filters):
    """
    Retrieve differences between two model's filter sections

    :param updated_model_component_filters: The "filters" key from the updated model
    :type updated_model_component_filters: Dict
    :param active_model_component_filters: The "Filters" key from the active model
    :type active_model_component_filters: Dict
    :return: Difference between filters
    :rtype: Dict
    """
    differences = {}
    filter_keys_to_ignore = ('id', 'cfid', 'cfhid')

    updated_model_component_filters_sorted = sorted(updated_model_component_filters,
                                                    key=lambda component_filter: component_filter['id'])
    active_model_component_filters_sorted = sorted(active_model_component_filters,
                                                   key=lambda component_filter: component_filter['id'])

    if len(updated_model_component_filters_sorted) > len(active_model_component_filters_sorted):
        differences['nr_of_filters_added'] = len(updated_model_component_filters_sorted) - \
                                             len(active_model_component_filters_sorted)

    if len(updated_model_component_filters_sorted) < len(active_model_component_filters_sorted):
        differences['nr_of_filters_removed'] = len(active_model_component_filters_sorted) - \
                                               len(updated_model_component_filters_sorted)

    if len(updated_model_component_filters_sorted) != len(active_model_component_filters_sorted):
        # This needs to be done to make sure DictDiffer compares correct objects
        updated_model_component_filters_sorted, active_model_component_filters_sorted = \
            fill_missing_filters(updated_model_component_filters_sorted,
                                 active_model_component_filters_sorted)

    for index, active_model_component_filter in enumerate(active_model_component_filters_sorted):

        # Looping with an index works because we first fill any missing filters. This means
        # we always have equal length active_model_component_filters and updated_model_component_filters
        updated_model_component_filter = updated_model_component_filters_sorted[index]

        for key_to_delete in filter_keys_to_ignore:
            updated_model_component_filter.pop(key_to_delete, None)
            active_model_component_filter.pop(key_to_delete, None)

        changes = [change for change in diff(active_model_component_filter, updated_model_component_filter)]
        if changes:
            # Check both to ensure also newly added display filters are
            # put under the 'display' key
            if active_model_component_filter['comparator'] == 'display' or \
                    updated_model_component_filter['comparator'] == 'display':
                if 'display' in differences:
                    differences['display'].append(changes)
                else:
                    differences['display'] = [changes]
                # Needed because we otherwise still process the active or updated model
                # component in the else clause because one of those could be false.
                continue
            else:
                if 'rules' in differences:
                    differences['rules'].append(changes)
                else:
                    differences['rules'] = [changes]

    return differences


def fill_missing_filters(updated_model_component_filters_sorted, active_model_component_filters_sorted):
    """
    Function to ensure both model filters have the same number of filters in order for
    the DictDiffer to do its work. Where needed an empty filter with a corresponding
    id are added.

    :param updated_model_component_filters_sorted: The "filters" key of a component of the updated model
    :type updated_model_component_filters_sorted: Dict
    :param active_model_component_filters_sorted: The "fiters" key of a component of the active model
    :type active_model_component_filters_sorted: Dict
    :return: Updated model component filters and Active model component
    :rtype: Tuple
    """
    active_ids = [active_filter['id'] for active_filter in active_model_component_filters_sorted]
    updated_ids = [updated_filter['id'] for updated_filter in updated_model_component_filters_sorted]

    filters_removed = list(set(active_ids) - set(updated_ids))
    filters_added = list(set(updated_ids) - set(active_ids))

    for index, active_filter in enumerate(active_model_component_filters_sorted):
        if active_filter['id'] in filters_removed:
            dict_to_add = dict.fromkeys(active_filter)
            dict_to_add['id'] = active_filter['id']
            updated_model_component_filters_sorted.insert(index, dict_to_add)

    for index, updated_filter in enumerate(updated_model_component_filters_sorted):
        if updated_filter['id'] in filters_added:
            dict_to_add = dict.fromkeys(updated_filter)
            dict_to_add['id'] = updated_filter['id']
            active_model_component_filters_sorted.insert(index, dict_to_add)

    return updated_model_component_filters_sorted, active_model_component_filters_sorted


def get_model_policy_differences(updated_model_policy, active_model_policy):
    """
    Retrieve differences between two model's "Policy" section. The policy section can be
    considered the model base.

    :param updated_model_policy: The "policy" key of the updated model
    :type updated_model_policy: Dict
    :param active_model_policy: The "policy" key of the active model
    :type active_model_policy: Dict
    :return: Differences between policies
    :rtype: Dict
    """
    policy_keys_to_ignore = ('history', 'pid', 'uuid', 'phid', 'active', 'modified',
                             'activeTimes', 'created', 'edited', 'version', 'logic',
                             'actions', 'tags', 'message')

    active_model_policy_actions_sorted = collections.OrderedDict(sorted(active_model_policy['actions'].items()))
    updated_model_policy_actions_sorted = collections.OrderedDict(sorted(updated_model_policy['actions'].items()))

    tag_changes = get_model_tag_differences(updated_model_policy['tags'], active_model_policy['tags'])
    action_changes = [change for change in diff(active_model_policy_actions_sorted,
                                                updated_model_policy_actions_sorted)]
    component_weight_changes = get_logic_weight_differences(active_model_policy['logic']['data'],
                                                            updated_model_policy['logic']['data'])

    differences = {}
    if tag_changes:
        differences['tags'] = tag_changes

    if action_changes:
        differences['actions'] = action_changes

    if component_weight_changes:
        differences['component_weight_changes'] = component_weight_changes

    for key_to_delete in policy_keys_to_ignore:
        updated_model_policy.pop(key_to_delete, None)
        active_model_policy.pop(key_to_delete, None)

    base_changes = [change for change in diff(active_model_policy, updated_model_policy)]

    if base_changes:
        differences['base'] = base_changes

    return differences


def get_model_tag_differences(updated_model_policy_tags, active_model_policy_tags):
    """
    Retrieve differences between two model's "tag" keys

    :param updated_model_policy_tags: The "tag" key of the updated model
    :type updated_model_policy_tags: Dict
    :param active_model_policy_tags: The "tag" key of the active model
    :type active_model_policy_tags: Dict
    :return: Tag differences
    :rtype: Dict
    """
    differences = {}
    for tag in active_model_policy_tags:
        if tag not in updated_model_policy_tags:
            if 'removed_tags' in differences:
                differences['removed_tags'].append(tag)
            else:
                differences['removed_tags'] = [tag]

    for tag in updated_model_policy_tags:
        if tag not in active_model_policy_tags:
            if 'added_tags' in differences:
                differences['added_tags'].append(tag)
            else:
                differences['added_tags'] = [tag]
    return differences


def get_model_action_differences(updated_model_policy_actions, active_model_policy_actions):
    """
    Retrieve differences between two model's "action" section

    :param updated_model_policy_actions: The "actions" key of the updated model
    :type updated_model_policy_actions: Dict
    :param active_model_policy_actions: The "actions" key of the active model
    :type active_model_policy_actions: Dict
    :return: Action differences
    :rtype: Dict
    """
    keys_to_ignore = []
    differences = {}

    for key in active_model_policy_actions.keys():
        if key in keys_to_ignore:
            continue

        try:
            if active_model_policy_actions[key] != updated_model_policy_actions[key]:
                differences[key] = updated_model_policy_actions[key]
        except KeyError:
            differences['added_or_removed_action'] = key
    return differences


def get_logic_weight_differences(active_model_policy_logic_data, updated_model_policy_logic_data):
    """
    Retrieve differences between two model's logic weights

    :param active_model_policy_logic_data: The "data" key of the active model policy->logic dict
    :type active_model_policy_logic_data: Dict
    :param updated_model_policy_logic_data: The "data" key of the update model policy->logic dict
    :type updated_model_policy_logic_data: Dict
    :return: Logic weight differences
    :rtype: Dict
    """
    differences = {}
    if len(updated_model_policy_logic_data) > len(active_model_policy_logic_data):
        differences['nr_of_weights_added'] = len(updated_model_policy_logic_data) - \
                                             len(active_model_policy_logic_data)

    if len(updated_model_policy_logic_data) < len(active_model_policy_logic_data):
        differences['nr_of_weights_removed'] = len(active_model_policy_logic_data) - \
                                               len(updated_model_policy_logic_data)

    if len(updated_model_policy_logic_data) != len(active_model_policy_logic_data):
        # The CID's always change, so we cannot compare. This leaves only the rule weights and nr of rules
        # that we can effectively compare. However, the rule weights are effectively a list of integers after
        # removing the CIDs. Unfortunately, comparing lists has all sorts of problems.
        #
        # Our assumption is that Darktrace orders the policy logic data list always the same.
        # This means that if we have an unequal number, we cannot "reliably" compare.
        # As such, we just return with the removed/added messages.
        return differences

    weights_to_compare = []

    for rule in active_model_policy_logic_data:
        if isinstance(rule, dict):
            weights_to_compare.append(rule['weight'])

    for index, rule in enumerate(updated_model_policy_logic_data):
        if not weights_to_compare:
            if isinstance(rule, dict):
                differences['component_{0}'.format(index)] = ('removed', rule['weight'])
            else:
                continue

        if isinstance(rule, dict):
            try:
                if rule['weight'] != weights_to_compare[index]:
                    differences['component_{0}'.format(index)] = ('changed', rule['weight'])
            except IndexError:
                differences['component_{0}'.format(index)] = ('added', rule['weight'])
    return differences

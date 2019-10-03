"""Functions used by the Click system subcommand"""
import fnmatch


def get_tags(api, **kwargs):
    """
    List of tags currently configured within Darktrace

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :return: Dictionary that contains all tags
    :rtype: Dict
    """
    return api.get('/tags', **kwargs)


def modify_device_tags(api, action, tag, did):
    """
    Add or remove device tag

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param action: Action to take (add or delete)
    :type action: String
    :param tag: Tag to be added to device
    :type tag: String
    :param did: Device identifier
    :type did: Integer
    :return: Dictionary that contains all tags
    :rtype: Dict
    """
    if action == 'add':
        return api.post('/tags/entities', postdata={'did': did, 'tag': tag}, did=did, tag=tag)

    # action == 'delete':
    return api.delete('/tags/entities', tag=tag, did=did)


def search_tags(api, name_query, devices_tagged_with):
    """
    Function to search for tags by name query or to search for devices tagged
    with tag.

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :param name_query: Shell-style search string potentially containing wildcards
    :type name_query: String
    :param devices_tagged_with:
    :type devices_tagged_with:
    :return: Found devices or tags
    :rtype: List
    """
    #
    # This function actually has two different outputs. As such, from a design perspective
    # it might be better to split this function into two.
    #
    if devices_tagged_with:
        tagged_devices = api.get('/tags/entities', tag=devices_tagged_with)
        return tagged_devices

    if name_query:
        tags = api.get('/tags')
        found_tags = []

        for tag in tags:
            if fnmatch.fnmatch(tag['name'].lower(), name_query.lower()):
                found_tags.append(tag)

        return found_tags

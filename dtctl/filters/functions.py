# pylint: disable=C0325
"""Functions used by the Click filters subcommand"""


def get_filters(api):
    """
    Get all Darktrace filters

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :return: List of all filters
    """
    filters = api.get('/filtertypes')
    return filters

# pylint: disable=C0325
"""Functions used by the Click components subcommand"""


def get_components(api):
    """
    Get all Darktrace components

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :return: List of all components
    """
    components = api.get('/components')
    return components

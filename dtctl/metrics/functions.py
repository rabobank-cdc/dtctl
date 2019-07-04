# pylint: disable=C0325
"""Functions used by the Click metrics subcommand"""


def get_metrics(api):
    """
    Get all Darktrace metrics

    :param api: Darktrace API object with initialized config values
    :type api: Api
    :return: List of all metrics
    """
    metrics = api.get('/metrics')
    return metrics

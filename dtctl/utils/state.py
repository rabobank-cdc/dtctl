"""Class to maintain Click program state"""


class ProgramState:
    """Class to maintain Click program state"""

    def __init__(self, api_obj, debug, config, config_file):
        """Create the Program State"""
        self.api = api_obj
        self.debug = debug
        self.config = config
        self.config_file = config_file

    def get_api(self):
        """
        Retrieve dtapi.api object

        :return: Stored API object
        :rtype: Api
        """
        return self.api

    def get_config_file(self):
        """
        Retrieve configured or specified config file

        :return: Path to config file
        :rtype: String
        """
        return self.config_file

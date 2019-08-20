"""Convenience classes and methods for generating CEF logging"""
from datetime import datetime as dt


class Cef:
    """Convenience classes and methods for generating CEF logging"""

    MAPPING = {
        'System Usage': {
            'type': 'cs1Label',
            'label': 'cs2Label',
            'bandwidth': 'in',
            'memused': 'cn1Label',
            'connectionsPerMinuteCurrent': 'cn2Label',
            'cpu': 'cn3Label',
            'dtqueue': 'flexNumber1Label'
        },
        'Packet Loss': {
            'packet_loss': 'cfp1Label',
            'worker_drop_rate': 'cfp2Label'
        },
        'DHCP Quality': {
            'subnets_tracking_dhcp': 'cn1Label',
            'total_dhcp_quality': 'cn2Label',
            'average_dhcp_quality': 'cn3Label1'
        }
    }

    def __init__(self, device_event_class_id, name, severity=3):
        """Create CEF object for easy logging"""
        # CEF format
        # CEF:Version|Device Vendor|Device Product|Device Version|Device Event Class ID|Name|Severity|[Extension]

        # CEF Example
        # CEF:0|Security|threatmanager|1.0|100|worm successfully stopped|10|src=10.0.0.1 dst=2.1.2.2 spt=1232
        self.version = 0
        self.vendor = 'Darktrace'
        self.product = 'DCIP System Monitoring'
        self.device_version = '1.0'
        self.device_event_class_id = device_event_class_id
        self.name = name
        self.severity = severity

    def generate_log_line(self, json_object, timestamp_key, system_key):
        """
        Generate a single log line in CEF format. Loops through all items in the json_object
        to build a CEF compatible log line. Note that the json_object must have the keys
        that are specified in the MAPPING object.

        :param json_object: The object containing all log information. This object is looped through
        :type json_object: Dict
        :param timestamp_key: The name of the field to get timestamp information from
        :type timestamp_key: String
        :param system_key: The name of the field to get the system name from
        :type system_key: String
        :return: Single log line in CEF format
        :rtype: String
        """
        timestamp = dt.strptime(json_object.pop(timestamp_key), '%Y-%m-%dT%H:%M:%S')
        system_name = json_object.pop(system_key)
        ip_address = json_object.pop('ip', None)

        # CEF "Header" and default fields
        line = 'CEF:{version}|{vendor}|{product}|{device_version}|{class_id}|{name}|{severity}|end={ts} ' \
               'deviceExternalId={system} '\
            .format(
                version=self.version,
                vendor=self.vendor,
                product=self.product,
                device_version=self.device_version,
                class_id=self.device_event_class_id,
                name=self.name,
                severity=self.severity,
                ts=timestamp,
                system=system_name
            )

        if ip_address:
            line += 'dvc={ip} '.format(ip=ip_address)

        for key, value in json_object.items():
            if key not in self.MAPPING[self.name]:
                continue

            if 'Label' in self.MAPPING[self.name][key]:
                line += '{k}={v} '.format(k=self.MAPPING[self.name][key],
                                          v=key)

            # The Label key has already been added above if present.
            # However, we also need the value in the corresponding value field (without Label)
            # For this we replace "Label" with nothing. This also means that fields without Label
            # are automatically picked up correctly.
            line += '{k}={v} '.format(k=self.MAPPING[self.name][key].replace('Label', ''),
                                      v=self.escape_strings_for_cef(value))

        # Remove last whitespace as result of string concatenation
        return line.strip()

    def generate_logs(self, output, timestamp_key='timestamp', system_key='system'):
        """
        Main function of the Cef object. This function is called to generate and return
        a list of CEF log lines.

        :param output: List of JSON objects that need to be converted to CEF log lines
        :type output: List
        :param timestamp_key: Name of the key in the JSON object to get timestamp information from
        :type timestamp_key: String
        :param system_key: Name of the key in the JSON object to get system name from
        :type system_key: String
        :return: List of CEF log lines
        :rtype: List
        """
        if not isinstance(output, list):
            raise TypeError('Not a list')

        log_lines = []
        for json_object in output:
            cef_log_line = '{0}\n'.format(self.generate_log_line(json_object, timestamp_key, system_key))
            log_lines.append(cef_log_line)
        return log_lines

    def convert_to_custom_cef_fields(self, input_dict):
        """
        Function to convert a dictionary to a CEF compatible string
        with DeviceCustom fields.

        :param input_dict: Dictionary containing Key Value pairs in need of conversion
        :type input_dict: Dict
        :return: The CEF Extension string with DeviceCustom fields
        :rtype: String
        """
        string_counter = 0
        float_counter = 0
        number_counter = 0
        line = ''

        for key, value in input_dict.items():
            if isinstance(value, (list, dict, set)):
                raise TypeError('Nested objects are not supported')

            key = self.escape_strings_for_cef(key)
            value = self.escape_strings_for_cef(value)

            if isinstance(value, str):
                string_counter += 1
                line += 'cs{counter}Label={k} cs{counter}={v} '.format(counter=string_counter, v=value, k=key)

            elif isinstance(value, float):
                float_counter += 1
                line += 'cf{counter}Label={k} cf{counter}={v} '.format(counter=float_counter, v=value, k=key)

            elif isinstance(value, int):
                number_counter += 1
                line += 'cn{counter}Label={k} cn{counter}={v} '.format(counter=number_counter, v=value, k=key)

        return line.strip()

    @staticmethod
    def escape_strings_for_cef(line):
        """
        Function to escape strings to be CEF compatible

        The characters "\" and "=" need to be escaped

        :param line: The text for which characters need to be replaced
        :type line: String
        :return: Text with characters escaped
        :rtype: String
        """
        if isinstance(line, str):
            return line.translate(str.maketrans({
                '=': r'\=',
                '\\': '\\\\'
            }))

        return line

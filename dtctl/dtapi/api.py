"""Convenience classes and methods for interacting with Darktrace API"""
import hmac
import os
import sys
import json
try:
    from simplejson.errors import JSONDecodeError
except ImportError:
    from json import JSONDecodeError
import datetime as dt
import requests


class Api:
    """Convenience class for interacting with Darktrace API"""

    def __init__(self, address, public_key, private_key, cacert=None, insecure=False, debug=False):
        """Create Darktrace API object"""
        self.address = address
        self.public_key = public_key
        self.private_key = private_key
        self.insecure = insecure
        self.ca_cert = cacert
        self.debug = debug

    def get_signature(self, call, timestamp):
        """
        Generate a signature for use with Darktrace API

        :param call: The API endpoint call. E.g. /status
        :type call: String
        :param timestamp: Timestamp for generating the correct signature
        :type timestamp: DateTime
        :return: The calculated HMAC signature
        :rtype: String
        """
        msg = '\n'.join([call, self.public_key, timestamp])
        signature = hmac.new(self.private_key.encode('utf8'), msg=msg.encode('utf8'), digestmod='sha1')
        return signature.hexdigest()

    def get_headers(self, call, timestamp=None):
        """
        Construct HTTP headers required for communicating with Darktrace API

        :param call: The API endpoint call. E.g. /status
        :type call: String
        :param timestamp: Timestamp for generating the correct signature
        :type timestamp: DateTime
        :return: Headers required for Darktrace API
        :rtype: Dict
        """
        timestamp = timestamp or dt.datetime.utcnow().strftime('%Y%m%dT%H%M%S')
        return {
            'DTAPI-Token': self.public_key,
            'DTAPI-Date': timestamp,
            'DTAPI-Signature': self.get_signature(call, timestamp)
        }

    def post(self, call, **kwargs):
        """
        Perform a POST request to Darktrace API

        :param call: The API endpoint call. E.g. /status
        :type call: String
        :param kwargs: Arguments for the final HTTP request
        :type kwargs: Dict
        :return: Result of API call
        :rtype: Dict
        """
        post_data = kwargs.pop('postdata')
        req = requests.Request('POST', self.address + call, data=post_data, params=kwargs)
        prepped = req.prepare()
        headers = self.get_headers(prepped.path_url)
        prepped.headers = headers
        prepped.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        session = requests.Session()

        if self.debug:
            print_debug_message(prepped)

        if self.ca_cert and os.path.exists(self.ca_cert):
            verify = self.ca_cert
        else:
            verify = not self.insecure

        try:
            #
            # There currently is a bug in Requests that prevents us from using prepared Requests
            # in combination with sessions.
            #
            # resp = session.send(prepped, verify=verify)
            resp = session.post(self.address + call, data=post_data, headers=headers, verify=verify)
            resp.raise_for_status()
        except requests.exceptions.SSLError as err:
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as err:
            raise SystemExit('Error: Failed connecting to {0}'.format(self.address))
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        if resp.status_code in [200, 201]:
            try:
                return resp.json()
            except (json.decoder.JSONDecodeError, JSONDecodeError):
                body = resp.text
                if '<title>Darktrace | Login</title>' in body:
                    raise SystemExit('API endpoint not supported')
                return body
        else:
            raise SystemExit('Error in submitting data.\nStatus code: {0}'.format(resp.status_code))
        # Here to satisfy pylint
        return None

    def get(self, call, **kwargs):
        """
        Perform a GET request to Darktrace API

        :param call: The API endpoint call. E.g. /status
        :type call: String
        :param kwargs: Arguments for the final HTTP request
        :type kwargs: Dict
        :return: Result of API call
        :rtype: Dict
        """
        req = requests.Request('GET', self.address + call, params=kwargs)
        prepped = req.prepare()
        headers = self.get_headers(prepped.path_url)
        prepped.headers = headers
        session = requests.Session()

        if self.debug:
            print_debug_message(prepped)

        if self.ca_cert and os.path.exists(self.ca_cert):
            verify = self.ca_cert
        else:
            verify = not self.insecure

        try:
            resp = session.send(prepped, verify=verify)
            resp.raise_for_status()
        except requests.exceptions.SSLError as err:
            raise SystemExit(err)
        except requests.exceptions.ConnectionError as err:
            raise SystemExit('Error: Failed connecting to {0}'.format(self.address))
        except requests.exceptions.HTTPError as err:
            try:
                print(json.dumps(resp.json(), indent=4), file=sys.stderr)
            except (json.decoder.JSONDecodeError, JSONDecodeError):
                pass
            raise SystemExit(err)

        try:
            return resp.json()
        except (json.decoder.JSONDecodeError, JSONDecodeError):
            body = resp.text
            if '<title>Darktrace | Login</title>' in body:
                raise SystemExit('API endpoint not supported')
            return body


def make_curl_command(prepared_request):
    """
    Turn a prepared Request into a curl command.
    Generally used for debugging purposes

    :param prepared_request: Prepared Request
    :type prepared_request: Request
    :return: Curl command string
    :rtype: String
    """
    command = "curl -i -X {method} -H {headers} --insecure -d \"{data}\" \"{uri}\""
    method = prepared_request.method
    uri = prepared_request.url
    data = prepared_request.body
    headers = ['"{0}: {1}"'.format(key, value) for key, value in prepared_request.headers.items()]
    headers = " -H ".join(headers)
    return command.format(method=method, headers=headers, data=data, uri=uri)


def print_debug_message(prepared_request):
    print('Request URL:\n[-] {0}'.format(prepared_request.url))
    print('Test command:\n[-] {0}'.format(make_curl_command(prepared_request)))
    print()

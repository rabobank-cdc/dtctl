import pytest
import datetime as dt
from dtctl.dtapi.api import Api

HOST = 'http://127.0.0.1'
PUB_DTKEY = 'pub_dtkey'
PRIVKEY = 'privkey'
CACERT = '/test/path/to/cacert'
INSECURE = True
DEBUG = True
PRE_COMPUTED_SIGNATURE = 'aab1d2c0656c9da3910725a40c18ea7a0d221b54'


def test_missing_values():
    with pytest.raises(TypeError) as exc_info:
        _ = Api()

    assert isinstance(exc_info.value, TypeError)
    assert "__init__() missing 3 required positional arguments: " \
           "'address', 'public_key', and 'private_key'" in exc_info.value.args[0]


def test_default_values():
    api = Api(HOST, PUB_DTKEY, PRIVKEY)

    assert api.ca_cert is None
    assert not api.insecure
    assert not api.debug


def test_setting_values():
    api = Api(HOST, PUB_DTKEY, PRIVKEY, CACERT, INSECURE, DEBUG)

    assert api.address is HOST
    assert api.public_key is PUB_DTKEY
    assert api.private_key is PRIVKEY
    assert api.ca_cert is CACERT
    assert api.insecure
    assert api.debug


def test_api_get_signature():
    api = Api(HOST, PUB_DTKEY, PRIVKEY)

    test_epoch = 1559566692  # 2019-01-01 01:00:00
    timestamp = dt.datetime.fromtimestamp(test_epoch).strftime('%Y%m%dT%H%M%S')

    assert PRE_COMPUTED_SIGNATURE == api.get_signature('/status', timestamp)


def test_get_headers():
    api = Api(HOST, PUB_DTKEY, PRIVKEY)

    test_epoch = 1559566692  # 2019-01-01 01:00:00
    timestamp = dt.datetime.fromtimestamp(test_epoch).strftime('%Y%m%dT%H%M%S')

    headers = api.get_headers('/status', timestamp)

    assert headers['DTAPI-Token'] == PUB_DTKEY
    assert headers['DTAPI-Date'] == timestamp
    assert headers['DTAPI-Signature'] == PRE_COMPUTED_SIGNATURE


def test_post_request_with_debug(capsys, requests_mock):
    api = Api(HOST, PUB_DTKEY, PRIVKEY, CACERT, INSECURE, DEBUG)
    entry = 'test.test.test'

    success_respone = {
        'response': 'SUCCESS',
        'added': 1,
        'updated': 0
    }

    requests_mock.post(HOST + '/intelfeed?addentry', json=success_respone)
    result = api.post('/intelfeed', postdata={'addentry': entry}, addentry=entry)
    captured = capsys.readouterr()

    assert result['response'] == 'SUCCESS'
    assert result['added'] == 1
    assert result['updated'] == 0
    assert HOST + '/intelfeed?addentry={0}'.format(entry) in captured.out


def test_post_request(capsys, requests_mock):
    api = Api(HOST, PUB_DTKEY, PRIVKEY)
    entry = 'test.test.test'

    success_respone = {
        'response': 'SUCCESS',
        'added': 1,
        'updated': 0
    }

    requests_mock.post(HOST + '/intelfeed?addentry', json=success_respone)
    result = api.post('/intelfeed', postdata={'addentry': entry}, addentry=entry)
    captured = capsys.readouterr()

    assert result['response'] == 'SUCCESS'
    assert result['added'] == 1
    assert result['updated'] == 0
    assert HOST + '/intelfeed?addentry={0}'.format(entry) not in captured.out


def test_post_request_with_bad_status_code(requests_mock):
    api = Api(HOST, PUB_DTKEY, PRIVKEY)
    entry = 'test.test.test'

    requests_mock.post(HOST + '/intelfeed?addentry', text='504 Server Error: Gateway Time-out', status_code=504)
    with pytest.raises(SystemExit) as exc_info:
        _ = api.post('/intelfeed', postdata={'addentry': entry}, addentry=entry)

    assert str(exc_info.value.args[0]).startswith('504')


def test_get_request_with_debug(capsys, requests_mock):
    api = Api(HOST, PUB_DTKEY, PRIVKEY, CACERT, INSECURE, DEBUG)

    success_respone = {
        'key': 'value'
    }

    requests_mock.get(HOST + '/info', json=success_respone)
    result = api.get('/info', test='test')
    captured = capsys.readouterr()

    assert result['key'] == 'value'
    assert HOST + '/info?test=test' in captured.out


def test_get_request(capsys, requests_mock):
    api = Api(HOST, PUB_DTKEY, PRIVKEY)

    success_respone = {
        'key': 'value'
    }

    requests_mock.get(HOST + '/info', json=success_respone)
    result = api.get('/info', test='test')
    captured = capsys.readouterr()

    assert result['key'] == 'value'
    assert HOST + '/info?test=test' not in captured.out


def test_get_request_with_bad_status_code(requests_mock):
    api = Api(HOST, PUB_DTKEY, PRIVKEY)

    requests_mock.get(HOST + '/status', text='504 Server Error: Gateway Time-out', status_code=504)
    with pytest.raises(SystemExit) as exc_info:
        _ = api.get('/status')

    assert str(exc_info.value.args[0]).startswith('504')


def test_api_endpoint_not_supported(requests_mock):
    api = Api(HOST, PUB_DTKEY, PRIVKEY)
    entry = 'test.test.test'

    # Darktrace provides positive status_codes, even on redirects
    requests_mock.post(HOST + '/intelfeed?addentry', text='<title>Darktrace | Login</title>', status_code=200)
    requests_mock.get(HOST + '/non-supported-endpoint', text='<title>Darktrace | Login</title>', status_code=201)

    with pytest.raises(SystemExit) as exc_info:
        _ = api.post('/intelfeed', postdata={'addentry': entry}, addentry=entry)

    assert 'API endpoint not supported' == exc_info.value.args[0]

    with pytest.raises(SystemExit) as exc_info:
        _ = api.get('/non-supported-endpoint')

    assert 'API endpoint not supported' == exc_info.value.args[0]

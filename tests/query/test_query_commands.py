import json
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_successful_get(get_private_key, requests_mock):
    get_private_key.return_value = ''
    test_host = 'http://127.0.0.1'

    requests_mock.get(test_host + '/status', json='{"key": "value"}')
    result = runner.invoke(cli, ['-h', test_host, '-p', 'pubkey', '-s', 'privkey', 'query', 'get', '/status'])

    assert result.output == '"{\\"key\\": \\"value\\"}"\n'
    assert result.exit_code == 0

    # Test for without the slash
    result = runner.invoke(cli, ['-h', test_host, '-p', 'pubkey', '-s', 'privkey', 'query', 'get', 'status'])
    assert result.output == '"{\\"key\\": \\"value\\"}"\n'
    assert result.exit_code == 0


@patch('dtctl.cli.get_private_key')
def test_failing_get(get_private_key, requests_mock):
    get_private_key.return_value = ''
    test_host = 'http://127.0.0.1'

    requests_mock.get(test_host + '/non_existing', text='API endpoint not supported')
    result = runner.invoke(cli, ['-h', test_host, '-p', 'pubkey', '-s', 'privkey', 'query', 'get', '/non_existing'])

    assert 'API endpoint not supported' in result.output
    assert result.exit_code == 0


@patch('dtctl.cli.get_private_key')
def test_post(get_private_key, requests_mock):
    get_private_key.return_value = ''
    test_host = 'http://127.0.0.1'

    success_respone = {
        'response': 'SUCCESS',
        'added': 1,
        'updated': 0
    }

    requests_mock.post(test_host + '/intelfeed?addentry=test.intern.local', json=success_respone)

    result = runner.invoke(cli, ['-h', test_host, '-p', 'pubkey', '-s', 'privkey', 'query', 'post',
                                 '/intelfeed?addentry=test.intern.local', '-b', 'addentry=test.intern.local'])

    assert json.loads(result.output) == success_respone

from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_details_missing_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'details'])

    # Note: Need to match for 'cli' instead of 'dtctl' because of how the runner invokes the cli.
    assert result.exit_code is 0
    assert 'Usage: cli details [OPTIONS] COMMAND [ARGS]...' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_wrong_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'details', 'non-existing'])

    assert result.exit_code is not 0
    assert 'Error: No such command "non-existing".' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_missing_breach_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'details', 'breach'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "PBID".' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_wrong_breach_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'details', 'breach', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "PBID": wrong is not a valid integer' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_missing_connection_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'details', 'connection'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "UID".' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_missing_device_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'details', 'device'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "DID".' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_wrong_device_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'details', 'device', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "DID": wrong is not a valid integer' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_missing_host_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'details', 'host'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "HOSTNAME".' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_wrong_host_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'details', 'host', '!wrong'])

    assert result.exit_code is not 0
    assert 'Error: Hostname contains invalid characters' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_missing_msg_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'details', 'msg'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "TEXT".' in result.output

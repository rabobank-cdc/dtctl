from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_devices_missing_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'devices'])

    # Note: Need to match for 'cli' instead of 'dtctl' because of how the runner invokes the cli.
    assert result.exit_code is 0
    assert 'Usage: cli devices [OPTIONS] COMMAND [ARGS]...' in result.output


@patch('dtctl.cli.get_private_key')
def test_devices_missing_list_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'devices', 'list', '-d', 'non-integer'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "--days" / "-d": non-integer is not a valid integer' in result.output


@patch('dtctl.cli.get_private_key')
def test_devices_missing_info_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'devices', 'info'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "DID"' in result.output


@patch('dtctl.cli.get_private_key')
def test_devices_wrong_info_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'devices', 'info', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "DID": wrong is not a valid integer' in result.output

from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_config_missing_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'config'])

    # Note: Need to match for 'cli' instead of 'dtctl' because of how the runner invokes the cli.
    assert result.exit_code is 0
    assert 'Usage: cli config [OPTIONS] COMMAND [ARGS]...' in result.output


@patch('dtctl.cli.get_private_key')
def test_config_missing_get_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'config', 'get'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "[secure-dtkey|dtkey|pub-dtkey|host|cacert]".' in result.output


@patch('dtctl.cli.get_private_key')
def test_config_wrong_get_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'config', 'get', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "[secure-dtkey|dtkey|pub-dtkey|host|cacert]": ' \
           'invalid choice: wrong.' in result.output


@patch('dtctl.cli.get_private_key')
def test_config_missing_set_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'config', 'set'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "[secure-dtkey|dtkey|pub-dtkey|host|cacert]".' in result.output


@patch('dtctl.cli.get_private_key')
def test_config_wrong_set_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'config', 'set', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "[secure-dtkey|dtkey|pub-dtkey|host|cacert]": ' \
           'invalid choice: wrong.' in result.output

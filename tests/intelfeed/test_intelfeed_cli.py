from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_intelfeed_missing_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'intelfeed'])

    # Note: Need to match for 'cli' instead of 'dtctl' because of how the runner invokes the cli.
    assert result.exit_code is 0
    assert 'Usage: cli intelfeed [OPTIONS] COMMAND [ARGS]...' in result.output


@patch('dtctl.cli.get_private_key')
def test_intelfeed_wrong_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'intelfeed', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: No such command "wrong".' in result.output


@patch('dtctl.cli.get_private_key')
def test_intelfeed_missing_add_option(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'intelfeed', 'add'])

    assert result.exit_code is not 0
    assert 'Error: Please provide an input option' in result.output

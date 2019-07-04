from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_filters_missing_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'filters'])

    # Note: Need to match for 'cli' instead of 'dtctl' because of how the runner invokes the cli.
    assert result.exit_code is 0
    assert 'Usage: cli filters [OPTIONS] COMMAND [ARGS]...' in result.output


@patch('dtctl.cli.get_private_key')
def test_filters_wrong_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'filters', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: No such command "wrong".' in result.output


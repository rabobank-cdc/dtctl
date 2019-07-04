from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_breaches_missing_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'breaches'])

    # Note: Need to match for 'cli' instead of 'dtctl' because of how the runner invokes the cli.
    assert result.exit_code is 0
    assert 'Usage: cli breaches [OPTIONS] COMMAND [ARGS]...' in result.output


@patch('dtctl.cli.get_private_key')
def test_breaches_wrong_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'breaches', 'non-existing'])

    assert result.exit_code is not 0
    assert 'Error: No such command "non-existing".' in result.output


@patch('dtctl.cli.get_private_key')
def test_breaches_missing_list_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'breaches', 'list'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "[all|acknowledged]".' in result.output


@patch('dtctl.cli.get_private_key')
def test_breaches_wrong_list_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'breaches', 'list', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "[all|acknowledged]": invalid choice: wrong. ' \
           '(choose from all, acknowledged)' in result.output


@patch('dtctl.cli.get_private_key')
def test_breaches_missing_report_arguments(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'breaches', 'report'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "[brief|commented|acknowledged]".' in result.output


@patch('dtctl.cli.get_private_key')
def test_breaches_wrong_report_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'breaches', 'report', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "[brief|commented|acknowledged]": invalid choice: wrong. ' \
           '(choose from brief, commented, acknowledged)' in result.output

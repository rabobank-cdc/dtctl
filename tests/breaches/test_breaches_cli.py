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


@patch('dtctl.cli.get_private_key')
def test_exclusion_of_tags_and_minimal(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'breaches', 'list', '-t', 'test', '-m'])

    assert result.exit_code is not 0
    assert 'Error: "tags" is mutually exclusive with "minimal".\n' == result.output


@patch('dtctl.cli.get_private_key')
def test_exclusion_of_tags_and_pid(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'breaches', 'list', '-t', 'test', '-p', '1'])

    assert result.exit_code is not 0
    assert 'Error: "tags" is mutually exclusive with "pid".\n' == result.output


@patch('dtctl.cli.get_private_key')
def test_exclusion_of_score_and_pid(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'breaches', 'list', '-s', 0.1, '-p', '1'])

    assert result.exit_code is not 0
    assert 'Error: "minscore" is mutually exclusive with "pid".\n' == result.output

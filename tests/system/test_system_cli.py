from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_system_missing_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'system'])

    # Note: Need to match for 'cli' instead of 'dtctl' because of how the runner invokes the cli.
    assert result.exit_code is 0
    assert 'Usage: cli system [OPTIONS] COMMAND [ARGS]...' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_wrong_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'system', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: No such command "wrong".' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_missing_infile(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'system', 'coverage',
                                 '--network-col', 'test', '--netmask-col', 'test'])

    assert result.exit_code is not 0
    assert 'Error: Missing option "--infile" / "-i".' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_coverage_incorrect_columns(get_private_key):
    infile_sample = 'tests/data/subnet_input_list.csv'

    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'system', 'coverage',
                                 '--network-col', 'test', '--netmask-col', 'test', '--infile', infile_sample,
                                 '--format', 'csv'])

    assert result.exit_code is not 0
    assert 'Error: Error finding specified column(s) in CSV file' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_coverage_no_columns(get_private_key):
    infile_sample = 'tests/data/subnet_input_list.csv'

    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'system', 'coverage',
                                 '--infile', infile_sample, '--format', 'csv'])

    assert result.exit_code is not 0
    assert 'Error: please specify CSV columns to use' in result.output

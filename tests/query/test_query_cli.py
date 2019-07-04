from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_query_missing_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'query'])

    # Note: Need to match for 'cli' instead of 'dtctl' because of how the runner invokes the cli.
    assert result.exit_code is 0
    assert 'Usage: cli query [OPTIONS] COMMAND [ARGS]...' in result.output


@patch('dtctl.cli.get_private_key')
def test_query_wrong_subcommand(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'query', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: No such command "wrong".' in result.output


@patch('dtctl.cli.get_private_key')
def test_query_missing_get_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'query', 'get'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "ENDPOINT".' in result.output


@patch('dtctl.cli.get_private_key')
def test_query_missing_post_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'query', 'post'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "ENDPOINT".' in result.output


@patch('dtctl.cli.get_private_key')
def test_query_missing_post_body(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'query', 'post', '/endpoint'])

    assert result.exit_code is not 0
    assert 'Error: Missing option "--body" / "-b".' in result.output

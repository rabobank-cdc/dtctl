import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_config_command(get_private_key):
    get_private_key.return_value = ''
    # Due to the way CliRunner works, we need to
    # provide the -h and -p options when invoking.
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'config', '--help'])

    assert result.exit_code == 0
    assert 'Manage dtctl configurations' in result.output
    assert re.search(r'get\s+View', result.output)
    assert re.search(r'set\s+Set', result.output)


@patch('dtctl.cli.get_private_key')
def test_config_get_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'config', 'get', '--help'])

    assert result.exit_code == 0
    # Ensures that arguments additions fail the test
    assert '[secure-dtkey|dtkey|pub-dtkey|host|cacert]' in result.output
    assert 'Get a dtctl configuration option' in result.output
    assert 'Arguments:' in result.output
    assert re.search(r'secure-dtkey\s+Configure', result.output)
    assert re.search(r'pub-dtkey\s+Configure', result.output)
    assert re.search(r'cacert\s+Configure', result.output)
    assert re.search(r'dtkey\s+Configure', result.output)
    assert re.search(r'host\s+Configure', result.output)


@patch('dtctl.cli.get_private_key')
def test_config_set_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'config', 'set', '--help'])

    assert result.exit_code == 0
    # Ensures that arguments additions fail the test
    assert '[secure-dtkey|dtkey|pub-dtkey|host|cacert]' in result.output
    assert 'Set a dtctl configuration option' in result.output
    assert 'Arguments:' in result.output
    assert re.search(r'secure-dtkey\s+Configure', result.output)
    assert re.search(r'pub-dtkey\s+Configure', result.output)
    assert re.search(r'cacert\s+Configure', result.output)
    assert re.search(r'dtkey\s+Configure', result.output)
    assert re.search(r'host\s+Configure', result.output)
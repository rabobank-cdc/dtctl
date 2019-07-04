import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_details_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['details', '--help'])

    assert result.exit_code == 0
    assert 'View details of entities (represented as commands)' in result.output
    assert re.search(r'breach\s+Time', result.output)
    assert re.search(r'connection\s+Time', result.output)
    assert re.search(r'device\s+Time', result.output)
    assert re.search(r'host\s+Time', result.output)
    assert re.search(r'msg\s+Get', result.output)


@patch('dtctl.cli.get_private_key')
def test_details_breach_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['details', 'breach', '--help'])

    assert result.exit_code == 0
    assert 'details breach [OPTIONS] PBID' in result.output
    assert 'Time sorted list of connections and events for a breach' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_connection_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['details', 'connection', '--help'])

    assert result.exit_code == 0
    assert 'details connection [OPTIONS] UID' in result.output
    assert 'Time sorted list of events for a connection' in result.output
    assert 'Example: CcdXo43n8B75cdYyI5' in result.output

    # Options
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_device_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['details', 'device', '--help'])

    assert result.exit_code == 0
    assert 'details device [OPTIONS] DID' in result.output
    assert 'Time sorted list of connections and events for a device' in result.output

    # Options
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_host_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['details', 'host', '--help'])

    assert result.exit_code == 0
    assert 'details host [OPTIONS] HOSTNAME' in result.output
    assert 'Time sorted list of connections and events for an EXTERNAL host' in result.output

    # Options
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_details_msg_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['details', 'msg', '--help'])

    assert result.exit_code == 0
    assert 'details msg [OPTIONS] TEXT' in result.output
    assert 'Get notice event details for a specified message.' in result.output
    assert 'Example: USER123' in result.output

    # Options
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-o, --outfile PATH' in result.output
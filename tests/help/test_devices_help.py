import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_devices_command(get_private_key):
    get_private_key.return_value = ''
    # Due to the way CliRunner works, we need to
    # provide the -h and -p options when invoking.
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'devices', '--help'])

    assert result.exit_code == 0
    assert 'List active devices identified by Darktrace' in result.output
    assert re.search(r'list\s+Returns', result.output)
    assert re.search(r'info\s+Returns', result.output)


@patch('dtctl.cli.get_private_key')
def test_devices_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'devices', 'list', '--help'])

    assert '-d, --days INTEGER' in result.output
    assert '-s, --seconds INTEGER' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_devices_info_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'devices', 'info', '--help'])

    assert re.search(r'DID\s+A', result.output)
    assert 'Usage: cli devices info [OPTIONS] DID' in result.output
    assert '-l, --full-device-details' in result.output
    assert '-o, --outfile PATH' in result.output

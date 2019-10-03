import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_tags_command(get_private_key):
    get_private_key.return_value = ''
    # Due to the way CliRunner works, we need to
    # provide the -h and -p options when invoking.
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'tags', '--help'])

    assert result.exit_code == 0
    assert 'Manage Darktrace tags' in result.output
    assert re.search(r'device\s+Add', result.output)
    assert re.search(r'list\s+List', result.output)
    assert re.search(r'search\s+Search', result.output)


@patch('dtctl.cli.get_private_key')
def test_tags_device_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'tags', 'device', '--help'])

    assert result.exit_code == 0
    assert 'Manage tags of a device' in result.output

    assert re.search(r'add\s+Add', result.output)
    assert re.search(r'delete\s+Delete', result.output)

    assert '-t, --tag TEXT' in result.output
    assert '-d, --did INTEGER' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_tags_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'tags', 'list', '--help'])

    assert result.exit_code == 0
    assert 'List all tags configured in Darktrace' in result.output

    assert '-t, --tag TEXT' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_tags_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'tags', 'search', '--help'])

    assert result.exit_code == 0
    assert 'Search tags or tagged entities' in result.output

    assert '-n, --name TEXT' in result.output
    assert '-t, --devices-tagged-with TEXT' in result.output
    assert '-o, --outfile PATH' in result.output

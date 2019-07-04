import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_filters_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['filters', '--help'])

    assert result.exit_code == 0
    assert 'View Darktrace filters' in result.output
    assert re.search(r'list\s+List', result.output)


@patch('dtctl.cli.get_private_key')
def test_filters_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['filters', 'list', '--help'])

    assert result.exit_code == 0
    assert 'List Darktrace component filters' in result.output

    # Options
    assert '-o, --outfile PATH' in result.output

import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_metrics_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['metrics', '--help'])

    assert result.exit_code == 0
    assert 'View Darktrace metrics' in result.output
    assert re.search(r'list\s+List', result.output)


@patch('dtctl.cli.get_private_key')
def test_metrics_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['metrics', 'list', '--help'])

    assert result.exit_code == 0
    assert 'List Darktrace metrics' in result.output

    # Options
    assert '-o, --outfile PATH' in result.output

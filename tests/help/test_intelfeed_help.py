import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_intelfeed_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['intelfeed', '--help'])

    assert result.exit_code == 0
    assert "Manage Darktrace's intelligence feeds" in result.output
    assert re.search(r'add\s+Add', result.output)
    assert re.search(r'list\s+List', result.output)


@patch('dtctl.cli.get_private_key')
def test_intelfeed_add_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['intelfeed', 'add', '--help'])

    assert result.exit_code == 0
    assert "Add an entry to Darktrace's intelligence feed (Watchlist)" in result.output
    assert 'add [OPTIONS] ENTRY' in result.output
    assert re.search(r'ENTRY\s+Hostname', result.output)


@patch('dtctl.cli.get_private_key')
def test_intelfeed_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['intelfeed', 'list', '--help'])

    assert result.exit_code == 0
    assert "List entries in Darktrace's intelligence feed (Watchlist)" in result.output
    assert '-o, --outfile PATH' in result.output

import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_intelfeed_command(get_private_key):
    get_private_key.return_value = ''
    # Due to the way CliRunner works, we need to
    # provide the -h and -p options when invoking.
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'intelfeed', '--help'])

    assert result.exit_code == 0
    assert "Manage Darktrace's intelligence feeds" in result.output
    assert re.search(r'add\s+Add', result.output)
    assert re.search(r'list\s+List', result.output)


@patch('dtctl.cli.get_private_key')
def test_intelfeed_add_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'intelfeed', 'add', '--help'])

    assert result.exit_code == 0
    assert "Add entries to Darktrace's intelligence feed (Watchlist)" in result.output
    assert '-v, --value TEXT' in result.output
    assert '-i, --infile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_intelfeed_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'intelfeed', 'list', '--help'])

    assert result.exit_code == 0
    assert "List entries in Darktrace's intelligence feed (Watchlist)" in result.output
    assert '-o, --outfile PATH' in result.output

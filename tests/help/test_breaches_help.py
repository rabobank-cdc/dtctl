import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_breaches_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['breaches', '--help'])

    assert result.exit_code == 0
    assert 'Commands for Darktrace model breaches' in result.output
    assert re.search(r'list\s+List', result.output)
    assert re.search(r'report\s+Generate', result.output)


@patch('dtctl.cli.get_private_key')
def test_breaches_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['breaches', 'list', '--help'])

    assert result.exit_code == 0
    assert 'List Darktrace model breaches' in result.output
    assert 'Arguments:' in result.output
    assert re.search(r'all\s+List', result.output)
    assert re.search(r'acknowledged\s+Only', result.output)


@patch('dtctl.cli.get_private_key')
def test_breaches_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['breaches', 'list', '--help'])

    assert result.exit_code == 0

    # Ensures that arguments additions fail the test
    assert '[all|acknowledged]' in result.output
    assert 'List Darktrace model breaches' in result.output
    assert 'Arguments:' in result.output
    assert re.search(r'all\s+List', result.output)
    assert re.search(r'acknowledged\s+Only', result.output)

    # Options
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_breaches_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['breaches', 'report', '--help'])

    assert result.exit_code == 0

    # Ensures that arguments additions fail the test
    assert '[brief|commented|acknowledged]' in result.output
    assert 'Generate reports for Darktrace model breaches' in result.output
    assert 'Arguments:' in result.output
    assert re.search(r'brief\s+Brief', result.output)
    assert re.search(r'commented\s+Only', result.output)
    assert re.search(r'acknowledged\s+Only', result.output)

    # Options
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-o, --outfile PATH' in result.output
    assert '-t, --template TEXT' in result.output
    assert '-f, --output [csv|xlsx]' in result.output

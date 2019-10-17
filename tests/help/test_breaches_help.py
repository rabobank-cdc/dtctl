import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_breaches_command(get_private_key):
    get_private_key.return_value = ''
    # Due to the way CliRunner works, we need to
    # provide the -h and -p options when invoking.
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'breaches', '--help'])

    assert result.exit_code == 0
    assert 'Commands for Darktrace model breaches' in result.output
    assert re.search(r'list\s+List', result.output)
    assert re.search(r'report\s+Generate', result.output)


@patch('dtctl.cli.get_private_key')
def test_breaches_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'breaches', 'list', '--help'])

    assert result.exit_code == 0
    assert 'List Darktrace model breaches' in result.output

    # Options
    assert '-a, --acknowledged' in result.output
    assert '-t, --tag TEXT' in result.output
    assert '-m, --minimal' in result.output
    assert '-s, --minscore FLOAT' in result.output
    assert '-p, --pid INTEGER' in result.output
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_breaches_report_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'breaches', 'report', '--help'])

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
    assert '-t, --template PATH' in result.output
    assert '-f, --output [csv|xlsx]' in result.output

import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_system_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['system', '--help'])

    assert result.exit_code == 0
    assert 'View internal Darktrace information' in result.output
    assert re.search(r'auditlog\s+Account', result.output)
    assert re.search(r'info\s+View', result.output)
    assert re.search(r'instances\s+View', result.output)
    assert re.search(r'status\s+Detailed', result.output)
    assert re.search(r'summary-statistics\s+Summary', result.output)
    assert re.search(r'tags\s+All', result.output)
    assert re.search(r'usage\s+Short', result.output)


@patch('dtctl.cli.get_private_key')
def test_system_auditlog_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['system', 'auditlog', '--help'])

    assert result.exit_code == 0
    assert 'Account audit log' in result.output
    assert '-s, --offset INTEGER' in result.output
    assert '-l, --limit INTEGER' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_info_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['system', 'info', '--help'])

    assert result.exit_code == 0
    assert 'View Darktrace system information such as time and version' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_instances_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['system', 'instances', '--help'])

    assert result.exit_code == 0
    assert 'View Darktrace instances, their labels, id numbers and potential locations.' in result.output
    assert '- Master id numbers are prepended to breach ids.' in result.output
    assert "- Location is determined by the Master's label." in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_status_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['system', 'status', '--help'])

    assert result.exit_code == 0
    assert 'Detailed status information of all instances and probes' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_summary_statistics_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['system', 'summary-statistics', '--help'])

    assert result.exit_code == 0
    assert 'Summary of Darktrace statistics' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_tags_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['system', 'tags', '--help'])

    assert result.exit_code == 0
    assert 'All tags configured in Darktrace' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_usage_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['system', 'usage', '--help'])

    assert result.exit_code == 0
    assert 'Short usage information of all instances and probes' in result.output
    assert '-o, --outfile PATH' in result.output
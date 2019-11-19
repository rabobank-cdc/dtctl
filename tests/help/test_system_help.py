import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_system_command(get_private_key):
    get_private_key.return_value = ''
    # Due to the way CliRunner works, we need to
    # provide the -h and -p options when invoking.
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', '--help'])

    assert result.exit_code == 0
    assert 'View internal Darktrace information' in result.output
    assert re.search(r'auditlog\s+Account', result.output)
    assert re.search(r'coverage\s+Calculate', result.output)
    assert re.search(r'info\s+View', result.output)
    assert re.search(r'instances\s+View', result.output)
    assert re.search(r'issues\s+View', result.output)
    assert re.search(r'packet-loss\s+View', result.output)
    assert re.search(r'status\s+Detailed', result.output)
    assert re.search(r'summary-statistics\s+Summary', result.output)
    assert re.search(r'tags\s+All', result.output)
    assert re.search(r'usage\s+Short', result.output)


@patch('dtctl.cli.get_private_key')
def test_system_auditlog_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', 'auditlog', '--help'])

    assert result.exit_code == 0
    assert 'Account audit log' in result.output
    assert '-s, --offset INTEGER' in result.output
    assert '-l, --limit INTEGER' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_info_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', 'info', '--help'])

    assert result.exit_code == 0
    assert 'View Darktrace system information such as time and version' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_instances_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', 'instances', '--help'])

    assert result.exit_code == 0
    assert 'View Darktrace instances, their labels, id numbers and potential locations.' in result.output
    assert '- Master id numbers are prepended to breach ids.' in result.output
    assert "- Location is determined by the Master's label." in result.output
    assert '-p, --show-probes' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_packet_loss_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', 'packet-loss', '--help'])

    assert result.exit_code == 0
    assert 'Information about reported packet loss per system' in result.output

    # Options
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-o, --outfile PATH' in result.output
    assert '--log' in result.output
    assert '--cef' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_status_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', 'status', '--help'])

    assert result.exit_code == 0
    assert 'Detailed status information of all instances and probes' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_summary_statistics_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', 'summary-statistics', '--help'])

    assert result.exit_code == 0
    assert 'Summary of Darktrace statistics' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_tags_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', 'tags', '--help'])

    assert result.exit_code == 0
    assert 'All tags configured in Darktrace' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_usage_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', 'usage', '--help'])

    assert result.exit_code == 0
    assert 'Short usage information of all instances and probes' in result.output
    assert '-o, --outfile PATH' in result.output
    assert '--log' in result.output
    assert '--cef' in result.output


@patch('dtctl.cli.get_private_key')
def test_system_coverage_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'system', 'coverage', '--help'])

    assert result.exit_code == 0
    assert 'Calculate coverage based on list of subnets expected to be monitored' in result.output
    assert 'Coverage calculation is quite simplistic and naive:' in result.output
    assert 'Coverage calculation is quite simplistic and naive:' in result.output
    assert 'a = nr of expected subnets to be monitored' in result.output
    assert 'b = nr of subnets seen by Darktrace that match an entry in the input file' in result.output
    assert 'coverage in percentage = a / b * 100' in result.output
    assert '-o, --outfile PATH' in result.output
    assert '-i, --infile PATH' in result.output
    assert '-f, --format [csv|text]' in result.output
    assert ' --network-col TEXT' in result.output
    assert ' --netmask-col TEXT' in result.output

    assert '--log' in result.output
    assert '--cef' in result.output

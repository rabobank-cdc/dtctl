import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_subnets_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['subnets', '--help'])

    assert result.exit_code == 0
    assert "View information of Darktrace's identified subnets" in result.output
    assert re.search(r'aggregates\s+Lists', result.output)
    assert re.search(r'devices\s+Nr', result.output)
    assert re.search(r'dhcp\s+Metrics', result.output)
    assert re.search(r'instances\s+Lists', result.output)
    assert re.search(r'list\s+Lists', result.output)
    assert re.search(r'unidirectional\s+Metrics', result.output)


@patch('dtctl.cli.get_private_key')
def test_subnets_aggregates_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['subnets', 'aggregates', '--help'])

    assert result.exit_code == 0
    assert "Lists the CIDR merged subnets without their meta data (IPv4 only)" in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_subnets_devices_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['subnets', 'devices', '--help'])

    assert result.exit_code == 0
    assert 'Nr of devices seen by Darktrace' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_subnets_dhcp_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['subnets', 'dhcp', '--help'])

    assert result.exit_code == 0
    assert 'Metrics for DHCP tracking' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_subnets_instances_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['subnets', 'instances', '--help'])

    assert result.exit_code == 0
    assert 'Lists subnets seen per Darktrace instance (IPv4 only)' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_subnets_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['subnets', 'list', '--help'])

    assert result.exit_code == 0
    assert 'List all subnets without their meta data (IPv4 only)' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_subnets_unidirectional_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['subnets', 'unidirectional', '--help'])

    assert result.exit_code == 0
    assert 'Metrics for unidirectional traffic' in result.output
    assert '-o, --outfile PATH' in result.output

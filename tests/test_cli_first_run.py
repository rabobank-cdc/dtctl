from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
@patch('dtctl.cli.load_config')
@patch('dtctl.config.commands.get_config_key')
def test_config_subcommand_without_host_and_pubkey(mock_get_config_key, mock_load_config, mock_get_private_key):
    mock_get_private_key.return_value = ''
    mock_load_config.return_value = {'cacert': '/path/to/cacert'}
    mock_get_config_key.return_value = {'cacert': '/path/to/cacert'}
    result = runner.invoke(cli, ['config', 'get', 'cacert'])

    assert result.exit_code == 0
    assert '/path/to/cacert' in result.output


@patch('dtctl.cli.get_private_key')
@patch('dtctl.cli.load_config')
def test_cli_missing_host(mock_load_config, mock_get_private_key):
    mock_get_private_key.return_value = ''
    mock_load_config.return_value = {}
    result = runner.invoke(cli, ['system', 'info'])

    assert result.exit_code != 0
    assert 'Error: Host not specified or configured' in result.output


@patch('dtctl.cli.get_private_key')
@patch('dtctl.cli.load_config')
def test_cli_missing_pubkey(mock_load_config, mock_get_private_key):
    mock_get_private_key.return_value = ''
    mock_load_config.return_value = {}
    result = runner.invoke(cli, ['--host', '127.0.0.1', 'system', 'info'])

    assert result.exit_code != 0
    assert 'Error: pub-dtkey not specified or configured' in result.output

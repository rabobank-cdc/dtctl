from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_models_missing_select_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'models', 'select'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "SELECTORS...".' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_wrong_select_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'models', 'select', 'wrong'])

    assert result.exit_code is not 0
    assert 'Invalid format for "wrong"' in result.output

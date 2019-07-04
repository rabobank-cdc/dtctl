from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_models_missing_report_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'models', 'report'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "[all|breach-summary]".' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_wrong_report_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'models', 'report', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "[all|breach-summary]": invalid choice: wrong.' in result.output

from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_models_missing_input_diff_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey', 'models', 'input-diff'])

    assert result.exit_code is not 0
    assert 'Error: Missing argument "[new|deleted|changed]".' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_wrong_input_diff_argument(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'models', 'input-diff', 'wrong'])

    assert result.exit_code is not 0
    assert 'Error: Invalid value for "[new|deleted|changed]": invalid choice: wrong.' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_missing_input_diff_arguments_option(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'models', 'input-diff', 'new'])

    assert result.exit_code is not 0
    assert 'Error: Missing option "--infile" / "-i".' in result.output

    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'models', 'input-diff', 'new'])

    assert result.exit_code is not 0
    assert 'Error: Missing option "--infile" / "-i".' in result.output

    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'models', 'input-diff', 'deleted'])

    assert result.exit_code is not 0
    assert 'Error: Missing option "--infile" / "-i".' in result.output

    result = runner.invoke(cli, ['-h', 'http://localhost', '-p', 'pubkey', '-s', 'privkey',
                                 'models', 'input-diff', 'changed'])

    assert result.exit_code is not 0
    assert 'Error: Missing option "--infile" / "-i".' in result.output

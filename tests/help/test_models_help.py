import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_models_command(get_private_key):
    get_private_key.return_value = ''
    # Due to the way CliRunner works, we need to
    # provide the -h and -p options when invoking.
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', '--help'])

    assert result.exit_code == 0
    assert 'View Darktrace models' in result.output
    assert re.search(r'autoupdatable\s+Models', result.output)
    assert re.search(r'input-diff\s+Shows', result.output)
    assert re.search(r'list\s+List', result.output)
    assert re.search(r'pending-updates\s+Models', result.output)
    assert re.search(r'report\s+Generate', result.output)
    assert re.search(r'search\s+Case', result.output)
    assert re.search(r'select\s+View', result.output)
    assert re.search(r'update-diff\s+Shows', result.output)
    assert re.search(r'updatable\s+Models', result.output)


@patch('dtctl.cli.get_private_key')
def test_models_autoupdatable_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', 'autoupdatable', '--help'])

    assert result.exit_code == 0
    assert 'List all models that have auto-update configured' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_input_diff_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', 'input-diff', '--help'])

    assert result.exit_code == 0

    # Ensures that arguments additions fail the test
    assert '[new|deleted|changed]' in result.output
    assert 'List differences in models based on a input list.' in result.output
    assert 'Example file contents:' in result.output
    assert 'Anomalous Connection::Data Sent to Rare Domain' in result.output
    assert 'SaaS::AWS::Anonymous S3 File Download' in result.output
    assert 'Arguments:' in result.output
    assert re.search(r'new\s+Models', result.output)
    assert re.search(r'deleted\s+Models', result.output)
    assert re.search(r'changed\s+Models', result.output)

    # Options
    assert '-i, --infile PATH' in result.output
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-e, --enhanced-only' in result.output
    assert '-a, --active-only' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_list_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', 'list', '--help'])

    assert result.exit_code == 0
    assert 'List all models present within Darktrace' in result.output

    # Options
    assert '-t, --tag TEXT' in result.output
    assert '-e, --enhanced-only' in result.output
    assert '-a, --active-only' in result.output
    assert '-w, --with-components' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_pending_updates_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', 'pending-updates', '--help'])

    assert result.exit_code == 0
    assert 'List all models that have updates pending' in result.output

    # Options
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_report_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', 'report', '--help'])

    assert result.exit_code == 0

    # Ensures that arguments additions fail the test
    assert '[all|breach-summary]' in result.output
    assert 'Generate report that lists models or breaches per model' in result.output
    assert 'Arguments:' in result.output
    assert re.search(r'all\s+Create', result.output)
    assert re.search(r'breach-summary\s+Create', result.output)

    # Options
    assert '-d, --days INTEGER' in result.output
    assert '--start-date [%d-%m-%Y]' in result.output
    assert '--end-date [%d-%m-%Y]' in result.output
    assert '-a, --active-only' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_search_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', 'search', '--help'])

    assert result.exit_code == 0

    # Ensures that arguments additions fail the test
    assert 'Usage: cli models search [OPTIONS]' in result.output
    assert ' Case-insensitive search for models' in result.output
    assert 'Examples:' in result.output
    assert 'dtctl models search --name *SMB*' in result.output
    assert 'dtctl models search --name Device*' in result.output
    assert 'dtctl models search --name ?evice*' in result.output

    # Options
    assert '-n, --name TEXT' in result.output
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_select_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', 'select', '--help'])

    assert result.exit_code == 0

    # Ensures that arguments additions fail the test
    assert 'Usage: cli models select [OPTIONS] SELECTORS...' in result.output
    assert 'Select models based on top-level key value pairs. Nesting is not possible.' in result.output
    assert 'Arguments:' in result.output
    assert re.search(r'SELECTORS\s+One', result.output)
    assert 'Examples:' in result.output
    assert re.search('dtctl models select active=true', result.output)
    assert re.search('dtctl models select autoupdate=true version=13', result.output)

    # Options
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_update_diff_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', 'update-diff', '--help'])

    assert result.exit_code == 0

    # Ensures that arguments additions fail the test
    assert 'List models that have updates pending and their respective changes' in result.output

    # Options
    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_models_updatable_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'models', 'updatable', '--help'])

    assert result.exit_code == 0
    assert 'List all models that can be updated without losing custom changes' in result.output
    assert '-o, --outfile PATH' in result.output
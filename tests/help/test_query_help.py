import re
from unittest.mock import patch
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


@patch('dtctl.cli.get_private_key')
def test_query_command(get_private_key):
    get_private_key.return_value = ''
    # Due to the way CliRunner works, we need to
    # provide the -h and -p options when invoking.
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'query', '--help'])

    assert result.exit_code == 0
    assert "Send direct HTTP requests to Darktrace API" in result.output
    assert re.search(r'get\s+Send', result.output)
    assert re.search(r'post\s+Send', result.output)


@patch('dtctl.cli.get_private_key')
def test_query_get_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'query', 'get', '--help'])

    assert result.exit_code == 0
    assert 'Send a GET request to Darktrace' in result.output

    # Ensures that arguments additions fail the test
    assert '[OPTIONS] ENDPOINT' in result.output
    assert re.search(r'ENDPOINT\s+The', result.output)

    assert 'Examples:' in result.output
    assert 'dtctl query get "/status"' in result.output
    assert 'dtctl query get "/breaches?starttime=1558303200000&endtime=1558475999000"' in result.output

    assert '-o, --outfile PATH' in result.output


@patch('dtctl.cli.get_private_key')
def test_query_post_command(get_private_key):
    get_private_key.return_value = ''
    result = runner.invoke(cli, ['-h', '_', '-p', '_', 'query', 'post', '--help'])

    assert result.exit_code == 0
    assert 'Send a POST request to Darktrace.' in result.output
    assert 'Note: The Darktrace API requires the body content to be reflected in the URL' in result.output

    # Ensures that arguments additions fail the test
    assert '[OPTIONS] ENDPOINT' in result.output
    assert re.search(r'ENDPOINT\s+The', result.output)

    assert 'Examples:' in result.output
    assert 'dtctl query post "/intelfeed?addentry=www.evildomain.com" -b addentry=www.evildomain.com' in result.output

    assert '-o, --outfile PATH' in result.output
    assert '-b, --body TEXT' in result.output

import re
from click.testing import CliRunner
from dtctl.cli import cli


runner = CliRunner()


def test_main_options():
    # Due to the way CliRunner works, we need to
    # provide the -h and -p options when invoking.
    result = runner.invoke(cli, ['-h', '_', '-p', '_', '--help'])

    assert result.exit_code == 0
    assert 'Darktrace Command Line Interface' in result.output
    assert '-v, --version' in result.output
    assert '-h, --host TEXT' in result.output
    assert '-p, --pub-dtkey TEXT' in result.output
    assert '-s, --priv-dtkey TEXT' in result.output
    assert '-e, --cacert TEXT' in result.output
    assert '-i, --insecure' in result.output
    assert '-d, --debug' in result.output
    assert '-c, --config-file TEXT' in result.output


def test_commands():
    result = runner.invoke(cli, ['-h', '_', '-p', '_', '--help'])

    assert result.exit_code == 0
    assert re.search(r'breaches\s+Commands', result.output)
    assert re.search(r'config\s+Manage', result.output)
    assert re.search(r'devices\s+List', result.output)
    assert re.search(r'intelfeed\s+Manage', result.output)
    assert re.search(r'models\s+View', result.output)
    assert re.search(r'query\s+Send', result.output)
    assert re.search(r'subnets\s+View', result.output)
    assert re.search(r'system\s+View', result.output)

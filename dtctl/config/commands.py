# pylint: disable=C0111
import click
from dtctl.config.operations import get_config_key
from dtctl.config.functions import set_dt_key, set_cacert, set_secure_dt_key, set_dt_public_key, set_dt_host


@click.command('set', short_help='Set a dtctl configuration option')
@click.argument('config-option', type=click.Choice(['secure-dtkey', 'dtkey', 'pub-dtkey', 'host', 'cacert']))
@click.option('--value', '-v', type=click.STRING, help='Value to configure for "config-option"', required=True)
@click.pass_obj
def set_config(program_state, config_option, value):
    """
    Set a dtctl configuration option

    \b
    Arguments:
        secure-dtkey    Configure the Darktrace private key in a secure manner
        pub-dtkey       Configure the Darktrace public key
        cacert          Configure a custom CA certificate
        dtkey           Configure the Darktrace private key insecurely NOT RECOMMENDED
        host            Configure the Darktrace host
    """
    if config_option == 'dtkey':
        set_dt_key(program_state.config_file)

    if config_option == 'secure-dtkey':
        set_secure_dt_key(program_state.config_file)

    if config_option == 'pub-dtkey':
        set_dt_public_key(program_state.config_file, value)

    if config_option == 'host':
        set_dt_host(program_state.config_file, value)

    if config_option == 'cacert':
        set_cacert(program_state.config_file, value)


@click.command('get', short_help='View value for a a configured dtctl option')
@click.argument('config-option', type=click.Choice(['secure-dtkey', 'dtkey', 'pub-dtkey', 'host', 'cacert']))
@click.pass_obj
def get_config(program_state, config_option):
    """
    Get a dtctl configuration option

    \b
    Arguments:
        secure-dtkey    Configure the Darktrace private key in a secure manner
        pub-dtkey       Configure the Darktrace public key
        cacert          Configure a custom CA certificate
        dtkey           Configure the Darktrace private key insecurely NOT RECOMMENDED
        host            Configure the Darktrace host
    """
    value = get_config_key(program_state.config_file, config_option)
    click.echo(value)

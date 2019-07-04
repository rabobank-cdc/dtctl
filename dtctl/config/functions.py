"""Functions used by the Click config subcommand"""
import getpass
import click
from dtctl.utils.crypto import encrypt, decrypt
from dtctl.config.operations import set_config_key, get_config_key


def get_cacert(config_file):
    """
    Get configured cacert file

    :param config_file: Path to config file
    :return: String value of cacert config item
    """
    return get_config_key(config_file, 'cacert')


def set_cacert(config_file, path_to_cacert):
    """
    Set configuration for cacert file

    :param config_file: Path to config file
    :param path_to_cacert: Path to custom cacert
    :return: None
    """
    set_config_key(config_file, 'cacert', path_to_cacert)


def get_secure_dt_key(config_file):
    """
    Retrieve decrypted value of Darktrace private API key

    :param config_file: Path to config file
    :return: String representing Darktrace private API key
    """
    click.echo('Decrypting Darktrace private key...')
    password = getpass.getpass('Enter password: ')
    value = decrypt(password, get_config_key(config_file, 'secure-dtkey'))
    return value


def set_dt_key(config_file):
    """
    Configure Daktrace private key insecurely in plain-text.
    Should only be used for non-interactive use

    :param config_file: Path to config file
    :return: None
    """
    dtkey = getpass.getpass('Enter Darktrace private key: ')
    set_config_key(config_file, 'dtkey', dtkey)


def set_secure_dt_key(config_file):
    """
    Configure Daktrace private key securely by storing an encrypted version

    :param config_file: Path to config file
    :return: None
    """
    privkey = getpass.getpass('Enter Darktrace private key: ')
    click.echo('-- Received Darktrace private key --')
    click.echo('Encrypting Darktrace private key with a password.')
    password = getpass.getpass('Enter password: ')
    verification_password = getpass.getpass('Retype password: ')

    if not password == verification_password:
        raise SystemExit('Error: Passwords did not match')

    encrypted_value = encrypt(password, privkey)
    set_config_key(config_file, 'secure-dtkey', encrypted_value)


def set_dt_public_key(config_file, pub_dtkey):
    """
    Configure Daktrace public key

    :param config_file: Path to config file
    :return: None
    """
    set_config_key(config_file, 'pub-dtkey', pub_dtkey)


def set_dt_host(config_file, host):
    """
    Configure Daktrace host name

    :param config_file: Path to config file
    :return: None
    """
    set_config_key(config_file, 'host', host)

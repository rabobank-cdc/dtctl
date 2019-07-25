"""Config operations module"""
import os
import sys
import json
import getpass
from pathlib import Path
from dtctl.utils.crypto import decrypt


def get_private_key(priv_dtkey, config_dict):
    """
    Determines where and how to retrieve the Darktrace private key
    and returns the key unencrypted to be used in Darktrace API calls
    in API calls

    :param priv_dtkey: The command line provided dtkey (None if not provided)
    :type priv_dtkey: String or None
    :param config_dict: The loaded configuration
    :type config_dict: Dict
    :return: Plain-text Darktrace private key
    :rtype: String
    """
    if priv_dtkey:
        # Private key provided on command line always takes precedence
        return priv_dtkey

    privkey = None

    if 'dtkey' not in config_dict and 'secure-dtkey' in config_dict:
        secure_dtkey = config_dict['secure-dtkey']
        password = getpass.getpass('Enter password to decrypt Darktrace private key: ')
        privkey = decrypt(password, secure_dtkey)

    if 'dtkey' in config_dict:
        print('WARNING: Using plaintext dtkey from config file.', file=sys.stderr)
        print('# Please use "dtctl config set --secure-dtkey"', file=sys.stderr)
        privkey = config_dict['dtkey']

    if not privkey:
        privkey = getpass.getpass('Please provide Darktrace private key: ')

    if not privkey:
        error_msg = 'Error: Unable to determine private key\n' \
                    '# Please configure a private key before using dtctl\n' \
                    '# - e.g.: dtctl config set --secure-dtkey'
        raise SystemExit(error_msg)

    return privkey


def load_config(config_file):
    """
    Load configuration from file

    :param config_file: Path to config file
    :return: Dict containing application configuration
    """
    config = {}

    if os.path.exists(config_file):
        with open(config_file, 'r') as infile:
            try:
                config = json.load(infile)
            except json.JSONDecodeError:
                raise SystemExit('Unable to parse config file\n{0}'.format(config_file))

    return config


def save_config(config_file, config):
    """
    Save configuration item

    :param config_file: Path to config file
    :param config: Dictionary containing all application configuration
    :return: None
    """
    if not os.path.exists(config_file):
        config_dir = os.path.dirname(config_file)
        Path(config_dir).mkdir(parents=True, exist_ok=True)

    with open(config_file, 'w') as outfile:
        json.dump(config, outfile, indent=4, sort_keys=True)


def set_config_key(config_file, key, value):
    """
    Configure a configuration key

    :param config_file: Path to config file
    :param key: Configuration item
    :param value: Configuration value
    :return: None
    """
    config = load_config(config_file)
    try:
        config[key] = value
    except KeyError:
        raise SystemExit('Mangled config file. Key: {0}'.format(key))

    save_config(config_file, config)


def get_config_key(config_file, key):
    """
    Retrieve configuration value

    :param config_file: Path to config file
    :param key: Configuration item
    :return: None
    """
    config = load_config(config_file)

    try:
        return config[key]
    except KeyError:
        return None

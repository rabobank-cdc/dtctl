"""Common functions for cryptography"""
from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Random import get_random_bytes


def encrypt(pass_phrase, data):
    """
    Encrypt data using a pass phrase

    :param pass_phrase: Pass phrase to encrypt data with
    :type pass_phrase: String
    :param data: Data to encrypt
    :type data: String
    :return: Formatted string that contains salt, iv and encrypted message
    :rtype: String
    """
    mode = AES.MODE_CBC
    block_size = AES.block_size
    salt = get_random_bytes(8)
    key = PBKDF2(pass_phrase, salt)
    body = Padding.pad(data.encode('utf-8'), block_size)
    initialization_vector = get_random_bytes(16)

    cipher = AES.new(key, mode, initialization_vector)

    # Now reassign salt, iv and body with their base64 encoded counterparts
    salt = b64encode(salt).decode('utf-8')
    initialization_vector = b64encode(initialization_vector).decode('utf-8')
    body = b64encode(cipher.encrypt(body)).decode('utf-8')

    return '{0}.{1}.{2}'.format(salt, initialization_vector, body)


def decrypt(pass_phrase, cipher_text):
    """
    Decrypt encrypted data with provided pass phrase

    :param pass_phrase: Pass phrase
    :type pass_phrase: String
    :param cipher_text: Encrypted data
    :type cipher_text: String
    :return: Decrypted data
    :rtype: String
    """
    mode = AES.MODE_CBC
    block_size = AES.block_size
    salt, initialization_vector, body = cipher_text.split('.')

    body = b64decode(body.encode('utf-8'))
    initialization_vector = b64decode(initialization_vector.encode('utf-8'))
    salt = b64decode(salt.encode('utf-8'))

    key = PBKDF2(pass_phrase, salt)
    cipher = AES.new(key, mode, initialization_vector)

    try:
        body = Padding.unpad(cipher.decrypt(body), block_size).decode('utf-8')
    except ValueError:
        # most likely a padding error which suggests incorrect password
        raise SystemExit('Password incorrect')
    return body

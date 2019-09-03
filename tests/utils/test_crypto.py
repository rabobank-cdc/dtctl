import pytest
from click import UsageError
from dtctl.utils.crypto import encrypt, decrypt


def test_encrypt():
    test_string = 'This is a test string for encryption'
    test_passphrase = 'G15#a@{lC[h~hC(bZ"IApvhI:zS3'
    encrypted_string = encrypt(test_passphrase, test_string)

    assert len(encrypted_string.split('.')) == 3
    assert decrypt(test_passphrase, encrypted_string) == test_string


def test_decrypt():
    test_string = 'This is a test string for decryption'
    test_passphrase = 'G15#a@{lC[h~hC(bZ"IApvhI:zS3'
    encrypted_string = encrypt(test_passphrase, test_string)

    assert decrypt(test_passphrase, encrypted_string) == test_string

    with pytest.raises(UsageError) as exc_info:
        decrypt('wrong_passphrase', encrypted_string)

    assert isinstance(exc_info.value, UsageError)
    assert exc_info.value.args[0] == 'Password incorrect'

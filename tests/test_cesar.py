from ciphers.cesar import CesarCipher

def test_atbash_cipher():
    assert 'Hello, world' == CesarCipher.decrypt_ascii(CesarCipher.encrypt_ascii('Hello, world', 5), 5)
    assert 'Hello, world' == CesarCipher.decrypt_unicode(CesarCipher.encrypt_unicode('Hello, world', 7), 7)
    print("ALL IS ALRIGHT")
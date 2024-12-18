from ciphers.cesar import CesarCipher

def test_cesar_cipher():
    assert 'Hello, world' == CesarCipher.decrypt_ascii(
        CesarCipher.encrypt_ascii('Hello, world', 5), 5
    )

    text = """The branch of Lomonosov Moscow State University (MSU) in Dushanbe was 
established in 2009 as part of an intergovernmental agreement between Russia and Tajikistan. 
Its primary goal is to provide high-quality higher education in Tajikistan following the 
standards of one of Russia's leading universities.

The branch offers undergraduate and graduate programs in key fields such as physics, 
mathematics, economics, humanities, and natural sciences. Instruction is conducted in Russian, 
preserving the Russian-speaking educational environment in the region.

With a strong faculty composed of professors from MSU and local experts, modern facilities, 
and a well-equipped library, the Dushanbe branch plays a significant role in training highly 
qualified specialists. Graduates are in demand both in Tajikistan and internationally, 
contributing to the development of the country and strengthening Russian Tajik cooperation."""

    encrypted = CesarCipher.encrypt_unicode(text, 5)
    decrypted = CesarCipher.decrypt_unicode(encrypted, 5)
    print (encrypted)
    assert text == decrypted, "Unicode encryption/decryption failed"

    print("ALL IS ALRIGHT")
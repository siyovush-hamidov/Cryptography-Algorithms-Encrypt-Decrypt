from ciphers.atbash import AtbashCipher

def test_atbash_cipher():
    assert AtbashCipher.reverse_message("Привет! Пока.") == ".акоП !тевирП"
    assert AtbashCipher.reverse_sentence("Привет, как дела? Пока.") == "?алед как ,тевирП.акоП "
    assert AtbashCipher.reverse_word("Привет! Пока.") == "тевирП! акоП."
    print("ALL IS ALRIGHT")
from ciphers import atbash_cipher

def test_atbash_cipher():
    assert atbash_cipher("HELLO") == "OLLEH"
    assert atbash_cipher("Привет! Я пишу программу.") == ".уммаргорп ушип Я !тевирП"
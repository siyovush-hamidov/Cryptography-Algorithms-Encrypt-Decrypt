from ciphers import PlayfairCipher

def test_playfair_encode():
    key = "playfair example"
    cipher = PlayfairCipher(key)

    # Простое шифрование
    assert cipher.playfair_encode("hide the gold") == "bmodzbxdnage"
    
    # Шифрование с повторяющимися буквами
    assert cipher.playfair_encode("balloon") == "dpyranqo"
    
    # Шифрование с заменой 'j' на 'i'
    assert cipher.playfair_encode("jump over the moon") == "rtifvaxezbxiqeqo"

def test_playfair_decode():
    key = "playfair example"
    cipher = PlayfairCipher(key)

    # Простое дешифрование
    assert cipher.playfair_decode("bmodzbxdnage") == "hidethegoldx"
    
    # Дешифрование с повторяющимися буквами
    assert cipher.playfair_decode("dpyranqo") == "balxloon"
    
    # Дешифрование текста с заменой 'j' на 'i'
    assert cipher.playfair_decode("rtifvaxezbxiqeqo") == "iumpoverthemoxon"
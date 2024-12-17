from ciphers import PlayfairCipher

key = "Gravity Falls"
cipher = PlayfairCipher(key)

plaintext = "Attack at dawn"
encrypted = cipher.playfair_encode(plaintext)
print("Encrypted:", encrypted)

decrypted = cipher.playfair_decode(encrypted)
print("Decrypted:", decrypted)

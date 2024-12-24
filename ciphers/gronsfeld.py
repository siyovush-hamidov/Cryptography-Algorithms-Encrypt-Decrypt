class GronsfeldCipher:
    characters = "".join(chr(i).encode('latin1').decode('cp1251', errors='replace') for i in range(32, 256))
    
    @staticmethod
    def _convert_key_to_numbers(key):
        """Преобразует строковый ключ в последовательность чисел."""
        return [ord(char) % 10 for char in key]

    @staticmethod
    def encrypt_ascii(text, key):
        """Шифрование текста с использованием шифра Гронсфельда."""
        key = GronsfeldCipher._convert_key_to_numbers(key)
        encrypted_text = ''
        
        for i, char in enumerate(text):
            if char in GronsfeldCipher.characters:
                shift = key[i % len(key)]
                new_index = (GronsfeldCipher.characters.index(char) + shift) % len(GronsfeldCipher.characters)
                encrypted_text += GronsfeldCipher.characters[new_index]
            else:
                encrypted_text += char  # Символы, которых нет в алфавите, остаются без изменений
        
        return encrypted_text
    
    @staticmethod
    def decrypt_ascii(text, key):
        """Дешифрование текста с использованием шифра Гронсфельда."""
        key = GronsfeldCipher._convert_key_to_numbers(key)
        decrypted_text = ''
        
        for i, char in enumerate(text):
            if char in GronsfeldCipher.characters:
                shift = key[i % len(key)]
                new_index = (GronsfeldCipher.characters.index(char) - shift) % len(GronsfeldCipher.characters)
                decrypted_text += GronsfeldCipher.characters[new_index]
            else:
                decrypted_text += char  # Символы, которых нет в алфавите, остаются без изменений
        
        return decrypted_text
    
# Пример использования
# plaintext = "hello mafaca its your time да да это твоё ублюдское время"
# key = "Hamidov"

# ciphertext = GronsfeldCipher.encrypt_ascii(plaintext, key)
# print("Зашифрованный текст:", ciphertext)

# decrypted_text = GronsfeldCipher.decrypt_ascii(ciphertext, key)
# print("Расшифрованный текст:", decrypted_text)    
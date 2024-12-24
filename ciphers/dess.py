class CustomDESCipher:
    charTable = [
        " ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a",
        "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "", "Ђ", "Ѓ", "‚",
        "ѓ", "„", "…", "†", "‡", "€", "‰", "Љ", "‹", "Њ", "Ќ", "Ћ", "Џ", "ђ", "‘", "’", "“", "”", "•", "–", "—", "", "™", "љ", "›", "њ", "ќ", "ћ", "џ", " ", "Ў", "ў",
        "Ј", "¤", "Ґ", "¦", "§", "Ё", "©", "Є", "«", "¬", "­", "®", "Ї", "°", "±", "І", "і", "ґ", "µ", "¶", "·", "ё", "№", "є", "»", "ј", "Ѕ", "ѕ", "ї", "А", "Б", "В", "Г",
        "Д", "Е", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д",
        "е", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"
    ]

    @staticmethod
    def validate_key(key):
        # Приведение ключа к длине 8 символов
        if len(key) < 8:
            key = (key * (8 // len(key) + 1))[:8]
        elif len(key) > 8:
            key = key[:8]

        if any(char not in CustomDESCipher.charTable for char in key):
            raise ValueError("Ключ содержит недопустимые символы.")

        return key

    @staticmethod
    def encrypt_ascii(plaintext, key):
        """
        Шифрует текст с использованием алфавита charTable.
        :param plaintext: Открытый текст для шифрования.
        :param key: Ключ для шифрования.
        :return: Зашифрованный текст в виде строки.
        """
        key = CustomDESCipher.validate_key(key)

        if any(char not in CustomDESCipher.charTable for char in plaintext):
            raise ValueError("Текст содержит символы, не входящие в поддерживаемый набор.")

        # Простая замена символов по ключу
        encrypted = ""
        for i, char in enumerate(plaintext):
            char_index = CustomDESCipher.charTable.index(char)
            key_index = CustomDESCipher.charTable.index(key[i % len(key)])
            encrypted_index = (char_index + key_index) % len(CustomDESCipher.charTable)
            encrypted += CustomDESCipher.charTable[encrypted_index]

        return encrypted

    @staticmethod
    def decrypt_ascii(ciphertext, key):
        """
        Дешифрует текст с использованием алфавита charTable.
        :param ciphertext: Зашифрованный текст в виде строки.
        :param key: Ключ для дешифрования.
        :return: Расшифрованный текст.
        """
        key = CustomDESCipher.validate_key(key)

        if any(char not in CustomDESCipher.charTable for char in ciphertext):
            raise ValueError("Текст содержит символы, не входящие в поддерживаемый набор.")

        # Обратная замена символов по ключу
        decrypted = ""
        for i, char in enumerate(ciphertext):
            char_index = CustomDESCipher.charTable.index(char)
            key_index = CustomDESCipher.charTable.index(key[i % len(key)])
            decrypted_index = (char_index - key_index) % len(CustomDESCipher.charTable)
            decrypted += CustomDESCipher.charTable[decrypted_index]

        return decrypted

# Пример использования
# if __name__ == "__main__":
#     key = "Ключ123"
#     cipher = CustomDESCipher(key)

#     plaintext = "Привет мир!"
#     encrypted_text = cipher.encrypt(plaintext)
#     print("Зашифрованный текст:", encrypted_text)

#     decrypted_text = cipher.decrypt(encrypted_text)
#     print("Расшифрованный текст:", decrypted_text)

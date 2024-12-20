class VerticalCipher:
    @staticmethod
    def encrypt_unicode(source_text: str, key: str) -> str:
        # Уникальные символы ключа
        unique_key = ''.join(sorted(set(key), key=lambda x: key.index(x)))
        sorted_key = ''.join(sorted(unique_key))

        columns = len(unique_key)
        rows = (len(source_text) + columns - 1) // columns  # Похоже на Math.Ceiling

        # Инициализация таблицы пробелами
        table = [[' ' for _ in range(columns)] for _ in range(rows)]

        k = 0
        for i in range(rows):
            for j in range(columns):
                if k < len(source_text):
                    table[i][j] = source_text[k]
                    k += 1

        cipher_text = ""
        for ch in sorted_key:
            index = unique_key.index(ch)
            for i in range(rows):
                cipher_text += table[i][index]

        return cipher_text

    @staticmethod
    def decrypt_unicode(cipher_text: str, key: str) -> str:
        source_text = ""
        # Уникальные символы ключа
        unique_key = ''.join(sorted(set(key), key=lambda x: key.index(x)))
        sorted_key = ''.join(sorted(unique_key))

        columns = len(unique_key)
        rows = (len(cipher_text) + columns - 1) // columns  # Похоже на Math.Ceiling

        # Инициализация таблицы пробелами
        table = [[' ' for _ in range(columns)] for _ in range(rows)]

        k = 0
        for ch in sorted_key:
            index = unique_key.index(ch)
            for i in range(rows):
                if k < len(cipher_text):
                    table[i][index] = cipher_text[k]
                    k += 1

        for i in range(rows):
            for j in range(columns):
                source_text += table[i][j]

        return source_text.strip()
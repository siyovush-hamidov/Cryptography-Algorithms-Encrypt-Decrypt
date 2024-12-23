class CaesarCipher:
    @staticmethod
    def encrypt_ascii(message: str, shift: int) -> str:
        result = ''

        # Составляем алфавит на основе символов от 32 до 255 в cp1251
        characters = "".join(chr(i).encode('latin1').decode(
            'cp1251', errors='replace') for i in range(32, 256))

        # Проходим по каждому символу сообщения
        for character in message:
            try:
                # Находим индекс символа в нашем алфавите
                index = characters.find(character)
                if index != -1:  # Если символ найден в алфавите
                    # Сдвигаем символ в пределах алфавита
                    new_char = characters[(index + shift) % len(characters)]
                    result += new_char
                else:
                    # Если символ не найден в алфавите, добавляем его без изменений
                    result += character
            except Exception as e:
                result += character
        return result

    @staticmethod
    def decrypt_ascii(message: str, shift: int) -> str:
        result = ''

        # Составляем алфавит на основе символов от 32 до 255 в cp1251
        characters = "".join(chr(i).encode('latin1').decode(
            'cp1251', errors='replace') for i in range(32, 256))

        # Проходим по каждому символу сообщения
        for character in message:
            try:
                # Находим индекс символа в нашем алфавите
                index = characters.find(character)
                if index != -1:  # Если символ найден в алфавите
                    # Сдвигаем символ в пределах алфавита в обратную сторону
                    new_char = characters[(index - shift) % len(characters)]
                    result += new_char
                else:
                    # Если символ не найден в алфавите, добавляем его без изменений
                    result += character
            except Exception as e:
                result += character
        return result

    @staticmethod
    def encrypt_unicode(text, shift):
        return ''.join(chr((ord(char) + shift) % 1114112) for char in text)

    @staticmethod
    def decrypt_unicode(text, shift):
        return ''.join(chr((ord(char) - shift) % 1114112) for char in text)

class CesarCipher:
    @staticmethod
    def encrypt_ascii(message: str, shift: int) -> str:
        result = ''
        for character in message:
            try:
                encoded_char = character.encode('Windows-1251')
                x = encoded_char[0]
                result += (bytes([(x + shift) % 256])).decode('Windows-1251')
            except (UnicodeEncodeError, IndexError):
                result += character
        return result

    @staticmethod
    def decrypt_ascii(message: str, shift: int) -> str:
        result = ''
        for character in message:
            try:
                encoded_char = character.encode('Windows-1251')
                x = encoded_char[0]
                result += (bytes([(x - shift) % 256])).decode('Windows-1251')
            except (UnicodeEncodeError, IndexError):
                result += character
        return result
    
    @staticmethod
    def encrypt_unicode(message: str, shift: int) -> str:
        result = ''
        for character in message:
            x = ord(character)
            result += chr((x + shift) % 0x110000)
        return result

    @staticmethod
    def decrypt_unicode(message: str, shift: int) -> str:
        result = ''
        for character in message:
            x = ord(character)
            result += chr((x - shift) % 0x110000)
        return result  

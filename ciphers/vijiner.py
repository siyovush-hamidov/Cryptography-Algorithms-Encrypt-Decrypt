class VigenereCipher:
    # Генерация таблицы Виженера
    @staticmethod
    def create_vigenere_table():
        # Генерация символов для cp1251 от 32 до 255
        cp1251_chars = [chr(i).encode('latin1').decode('cp1251', errors='replace') for i in range(32, 256)]
        table = []
        for i in range(len(cp1251_chars)):
            # Сдвигаем строку на i позиций
            row = cp1251_chars[i:] + cp1251_chars[:i]
            table.append(row)
        return table

    # Метод нормализации ключа
    @staticmethod
    def normalize_key(key: str, text: str) -> str:
        key = key.lower()

        # Убираем все символы, которые не входят в cp1251
        cp1251_chars = [chr(i).encode('latin1').decode('cp1251', errors='replace') for i in range(32, 256)]
        key = ''.join([char for char in key if char in cp1251_chars])

        # Если ключ короче текста, повторяем его
        if len(key) < len(text):
            repeat_times = len(text) // len(key) + 1
            key = (key * repeat_times)[:len(text)]
        elif len(key) > len(text):
            key = key[:len(text)]  # Обрезаем ключ до длины текста

        return key

    # Метод шифрования
    @staticmethod
    def encrypt_ascii(text: str, key: str) -> str:
        key = VigenereCipher.normalize_key(key, text)
        vigenere_table = VigenereCipher.create_vigenere_table()

        encrypted_text = []
        key_index = 0

        for i in range(len(text)):
            char = text[i]
            key_char = key[key_index % len(key)]

            # Находим индексы символов в первой строке таблицы
            row = vigenere_table[0].index(char)  # Индекс символа текста в первой строке
            col = vigenere_table[0].index(key_char)  # Индекс символа ключа в первой строке

            # Шифруем, используя сдвиг в таблице Виженера
            encrypted_text.append(vigenere_table[row][col])  # Берем символ по сдвигу в таблице
            key_index += 1

        return ''.join(encrypted_text)

    # Метод дешифрования
    @staticmethod
    def decrypt_ascii(encrypted_text: str, key: str) -> str:
        key = VigenereCipher.normalize_key(key, encrypted_text)
        vigenere_table = VigenereCipher.create_vigenere_table()

        decrypted_text = []
        key_index = 0

        for i in range(len(encrypted_text)):
            char = encrypted_text[i]
            key_char = key[key_index % len(key)]

            # Находим индексы символов в первой строке таблицы
            row = vigenere_table[0].index(key_char)  # Индекс символа ключа в первой строке
            col = vigenere_table[row].index(char)  # Находим индекс символа шифрованного текста в строке

            # Дешифруем, восстанавливаем исходный символ
            decrypted_text.append(vigenere_table[0][col])  # Берем символ из первой строки
            key_index += 1

        return ''.join(decrypted_text)

# Пример использования
# text = "Р!спийьвв'ьЯфаЫщопЭчрцшЭ,хЯ\"(в%в#сб&в#ЬьцпШп сиирц#Южшцля)ф(фмхцр-жежЫЬщоьв# ажвцЭусль@ШвжЭысрфопф&ф&воцпхсШьвв&нпзж !зф&фхцвжфсгщЬщт!Ыйщэрц&Ю(впняЮжлфопн&вфсяЭыицЭусии0цщЯЭч!тапЬщ)Ят!Ыькщьеаоц)пажефац0Я%ье%ф0ццхЯцЭ#ац а(Ь хупо%'цЫжщЫфутр'цЭюопьЫщгюЯэЭацЯь#бнь&вуцт!ЯцЭ#'ц тсрр!#буояЭчЭгьЯщЭюЭч0 йлЯ)хцЮттЯфхлй&воцпхсШьвЬFрцЯ)ьЬхпЯ ьЬв#вжЭысрфопф&б&воцпхсШьвв&пф#нЯщ бя)б#фмрцх Ыщ!а%ЯатЭф(бв&Я(зеэЭацЬ)звэЭ\"вб#)Яэоо%рцЯ)опц0Я%ье%ф&воцпхсШьвв&ц0фцЮ#в#ее(впнщЮ#бочии@уЯ%ье#брцшЭЫжЯ$ !ЭююЬ#Юуфщз\"вусоьЭ3хцжфжл&бЬццхспеЫжз#сйжхцраусЭ3!х ат т!Эюхф%пр!нпзж !р-гьЬьб&ц&пхЯ!ьЬЯ%ьвв&пс#ЮежЫжннэз!х#щтЮ@ущЫхфзш&вац#ЮЯш бт!Я%ье%ф\"вяЭЬъц%суежЬъцхщЮ#ЮЮ(цзт ц&ЭцЫыъЭоьв#нр&буцЮщатЭцщЫупчЭцхЭшфарнт!в(х,атомЫщьнацжл#Ю тн:"  # Текст для шифрования
# keys = ["Соли", "Шухрат", "Шарафзода",
#         "Соли Шухрат", "Соли Шарафзода", "Шухрат Соли", "Шухрат Шарафзода", "Шарафзода Шухрат", "Шарафзода Соли",
#         "Соли Шухрат Шарафзода", "Соли Шарафзода Шухрат", "Шухрат Соли Шарафзода", "Шухрат Шарафзода Соли", 
#         "Шарафзода Соли Шухрат", "Шарафзода Шухрат Соли"]  # Ключ для шифрования

# cipher = VigenereCipher()
# for key in keys:
#     encrypted_text = cipher.encrypt_ascii(text, key)
#     print(f"{key}: \nЗашифрованный текст: {encrypted_text}")

#     # Дешифруем текст
#     decrypted_text = cipher.decrypt_ascii(text, key)
#     print(f"{key}: \nДешифрованный текст: {decrypted_text}")

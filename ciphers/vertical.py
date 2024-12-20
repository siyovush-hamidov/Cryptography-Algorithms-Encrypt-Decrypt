import math

# Алфавит ascii
cp1251_chars = [chr(i).encode('latin1').decode('cp1251', errors='replace') for i in range(32, 256)]

class VerticalCipher:
    @staticmethod
    def encrypt_ascii(source_text: str, key: str) -> str:
        # Уникальные символы ключа
        unique_key = ''.join(sorted(set(key), key=lambda x: key.index(x)))
        sorted_key = ''.join(sorted(unique_key))

        columns = len(unique_key)
        rows = (len(source_text) + columns - 1) // columns  # Похоже на Math.Ceiling

        # Инициализация таблицы пробелами
        table = [[' ' for _ in range(columns)] for _ in range(rows)]

        # Заполнение таблицы
        k = 0
        for i in range(rows):
            for j in range(columns):
                if k < len(source_text):
                    table[i][j] = source_text[k]
                    k += 1

        # Чтение столбцов по отсортированному ключу
        cipher_text = ""
        for ch in sorted_key:
            index = unique_key.index(ch)
            for i in range(rows):
                cipher_text += table[i][index]

        return cipher_text

    @staticmethod
    def decrypt_ascii(cipher_text: str, key: str) -> str:
        source_text = ""
        # Уникальные символы ключа
        unique_key = ''.join(sorted(set(key), key=lambda x: key.index(x)))
        sorted_key = ''.join(sorted(unique_key))

        columns = len(unique_key)
        rows = (len(cipher_text) + columns - 1) // columns  # Похоже на Math.Ceiling

        # Инициализация таблицы пробелами
        table = [[' ' for _ in range(columns)] for _ in range(rows)]

        # Заполнение таблицы по отсортированному ключу
        k = 0
        for ch in sorted_key:
            index = unique_key.index(ch)
            for i in range(rows):
                if k < len(cipher_text):
                    table[i][index] = cipher_text[k]
                    k += 1

        # Чтение таблицы построчно
        for i in range(rows):
            for j in range(columns):
                source_text += table[i][j]

        return source_text.strip()

# Пример использования
# text = "Р!спийьвв'ьЯфаЫщопЭчрцшЭ,хЯ\"(в%в#сб&в#ЬьцпШп сиирц#Южшцля)ф(фмхцр-жежЫЬщоьв# ажвцЭусль@ШвжЭысрфопф&ф&воцпхсШьвв&нпзж !зф&фхцвжфсгщЬщт!Ыйщэрц&Ю(впняЮжлфопн&вфсяЭыицЭусии0цщЯЭч!тапЬщ)Ят!Ыькщьеаоц)пажефац0Я%ье%ф0ццхЯцЭ#ац а(Ь хупо%'цЫжщЫфутр'цЭюопьЫщгюЯэЭацЯь#бнь&вуцт!ЯцЭ#'ц тсрр!#буояЭчЭгьЯщЭюЭч0 йлЯ)хцЮттЯфхлй&воцпхсШьвЬFрцЯ)ьЬхпЯ ьЬв#вжЭысрфопф&б&воцпхсШьвв&пф#нЯщ бя)б#фмрцх Ыщ!а%ЯатЭф(бв&Я(зеэЭацЬ)звэЭ\"вб#)Яэоо%рцЯ)опц0Я%ье%ф&воцпхсШьвв&ц0фцЮ#в#ее(впнщЮ#бочии@уЯ%ье#брцшЭЫжЯ$ !ЭююЬ#Юуфщз\"вусоьЭ3хцжфжл&бЬццхспеЫжз#сйжхцраусЭ3!х ат т!Эюхф%пр!нпзж !р-гьЬьб&ц&пхЯ!ьЬЯ%ьвв&пс#ЮежЫжннэз!х#щтЮ@ущЫхфзш&вац#ЮЯш бт!Я%ье%ф\"вяЭЬъц%суежЬъцхщЮ#ЮЮ(цзт ц&ЭцЫыъЭоьв#нр&буцЮщатЭцщЫупчЭцхЭшфарнт!в(х,атомЫщьнацжл#Ю тн:"  # Текст для шифрования
# keys = ["Соли", "Шухрат", "Шарафзода",
#         "Соли Шухрат", "Соли Шарафзода", "Шухрат Соли", "Шухрат Шарафзода", "Шарафзода Шухрат", "Шарафзода Соли",
#         "Соли Шухрат Шарафзода", "Соли Шарафзода Шухрат", "Шухрат Соли Шарафзода", "Шухрат Шарафзода Соли", 
#         "Шарафзода Соли Шухрат", "Шарафзода Шухрат Соли"]  # Ключ для шифрования

# cipher = VerticalCipher()
# for key in keys:
#     encrypted_text = cipher.encrypt_ascii(text, key)
#     print(f"{key}: \nЗашифрованный текст: {encrypted_text}")

#     # Дешифруем текст
#     decrypted_text = cipher.decrypt_ascii(text, key)
#     print(f"{key}: \nДешифрованный текст: {decrypted_text}")
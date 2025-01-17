# from Crypto.Cipher import DES
# from Crypto.Util.Padding import pad, unpad
# import binascii

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

    def validate_key_unicode(key):
        # Приведение ключа к длине 8 символов
        if len(key) < 8:
            key = (key * (8 // len(key) + 1))[:8]
        elif len(key) > 8:
            key = key[:8]

        return key.encode('utf-8')

    @staticmethod
    def encrypt_unicode(plaintext, key):
        """
        Шифрует текст с использованием DES (встроенной библиотеки pycryptodome).
        :param plaintext: Открытый текст для шифрования.
        :param key: Ключ для шифрования.
        :return: Зашифрованный текст в виде строки (в 16-ричном формате).
        """
        key = CustomDESCipher.validate_key(key)

        # Приводим текст к байтам
        plaintext_bytes = plaintext.encode('utf-8')
        
        # Дополняем текст до кратности 8 байт (для DES)
        cipher = DES.new(key, DES.MODE_CBC)  # Инициализация в режиме CBC
        ciphertext = cipher.encrypt(pad(plaintext_bytes, DES.block_size))

        # Возвращаем шифрованный текст в 16-ричном виде и инициализационный вектор (IV)
        return binascii.hexlify(cipher.iv + ciphertext).decode('utf-8')

    @staticmethod
    def decrypt_unicode(ciphertext, key):
        """
        Дешифрует текст с использованием DES (встроенной библиотеки pycryptodome).
        :param ciphertext: Зашифрованный текст в виде строки (в 16-ричном формате).
        :param key: Ключ для дешифрования.
        :return: Расшифрованный текст.
        """
        key = CustomDESCipher.validate_key(key)

        # Декодируем из 16-ричного формата
        ciphertext_bytes = binascii.unhexlify(ciphertext)

        # Извлекаем инициализационный вектор (IV) из начала зашифрованного текста
        iv = ciphertext_bytes[:8]
        ciphertext_bytes = ciphertext_bytes[8:]

        # Дешифруем текст
        cipher = DES.new(key, DES.MODE_CBC, iv)
        plaintext_bytes = unpad(cipher.decrypt(ciphertext_bytes), DES.block_size)

        # Возвращаем расшифрованный текст
        return plaintext_bytes.decode('utf-8')


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

# # Пример использования
# # if __name__ == "__main__":
# #     key = "Ключ123"
# #     cipher = CustomDESCipher(key)

# #     plaintext = "Привет мир!"
# #     encrypted_text = cipher.encrypt(plaintext)
# #     print("Зашифрованный текст:", encrypted_text)

# #     decrypted_text = cipher.decrypt(encrypted_text)
# #     print("Расшифрованный текст:", decrypted_text)
import os


IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25]

# Таблицы расширения и P-бокса
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# S-боксы
S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2-S8 (добавьте остальные S-боксы)
]

def permute(block, table):
    """Выполняет перестановку битов согласно таблице"""
    return ''.join(block[i-1] for i in table)

def split_blocks(block):
    """Разделяет 64-битный блок на две 32-битные части"""
    return block[:32], block[32:]

def expand(block):
    """Расширяет 32-битный блок до 48 битов"""
    return permute(block, E)

def xor_strings(s1, s2):
    """Выполняет операцию XOR над двумя битовыми строками"""
    return ''.join('1' if c1 != c2 else '0' for c1, c2 in zip(s1, s2))
S_BOXES = [
    # S1
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    # S2
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    # S3
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    # S4
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    # S5
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    # S6
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    # S7
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    # S8
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

def s_box_substitute(expanded_block):
    """
    Выполняет замену через S-boxes
    """
    # Строка длиной 48 бит разбивается на 8 частей по 6 бит
    # Каждая часть преобразуется через соответствующий S-box в 4 бита
    result = ""
    for i in range(8):
        # Берем очередные 6 бит
        chunk = expanded_block[i*6:(i+1)*6]
        
        # Первый и последний биты определяют строку (2 бита -> число от 0 до 3)
        row = int(chunk[0] + chunk[5], 2)
        
        # Средние биты определяют столбец (4 бита -> число от 0 до 15)
        col = int(chunk[1:5], 2)
        
        # Получаем значение из соответствующего S-box
        value = S_BOXES[i][row][col]
        
        # Преобразуем в 4-битное двоичное число
        binary = format(value, '04b')
        result += binary
    
    return result

# [Previous implementation of other functions remains the same]

def f_function(block, subkey):
    """Функция Фейстеля"""
    # print(f"F-function input block length: {len(block)}")
    # print(f"F-function subkey length: {len(subkey)}")
    
    expanded = expand(block)
    # print(f"After expansion: {len(expanded)} bits")
    
    xored = xor_strings(expanded, subkey)
    # print(f"After XOR: {len(xored)} bits")
    
    substituted = s_box_substitute(xored)
    # print(f"After substitution: {len(substituted)} bits")
    
    result = permute(substituted, P)
    # print(f"After P-box: {len(result)} bits")
    
    return result


def decrypt_block(block, subkeys):
    """Расшифровывает один 64-битный блок"""
    block = permute(block, IP)
    left, right = split_blocks(block)
    
    # 16 раундов
    for i in range(15, -1, -1):  # Используем подключи в обратном порядке
        new_right = xor_strings(left, f_function(right, subkeys[i]))
        left = right
        right = new_right
    
    # Финальная перестановка
    final_block = right + left  # Обратите внимание на смену местами
    return permute(final_block, IP_INV)

PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5,
       3, 28, 15, 6, 21, 10,
       23, 19, 12, 4, 26, 8,
       16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

# Количество сдвигов для каждого раунда
SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def generate_subkeys(key):
    """
    Генерирует 16 48-битных подключей из 64-битного ключа
    """
    # Применяем PC1 перестановку
    key = permute(key, PC1)
    
    # Разделяем на левую и правую части
    left = key[:28]
    right = key[28:]
    
    subkeys = []
    
    # Генерируем 16 подключей
    for shift in SHIFT_SCHEDULE:
        # Циклический сдвиг влево
        left = left[shift:] + left[:shift]
        right = right[shift:] + right[:shift]
        
        # Объединяем части и применяем PC2
        combined = left + right
        subkey = permute(combined, PC2)
        
        subkeys.append(subkey)
    
    return subkeys

def decrypt_des(ciphertext, key):
    """Основная функция расшифровки"""
    # Преобразование шифротекста в битовую строку
    binary_ciphertext = ''.join(format(byte, '08b') for byte in ciphertext)
    
    # Генерация подключей
    subkeys = generate_subkeys(key)
    
    # Расшифровка по блокам
    plaintext = ''
    for i in range(0, len(binary_ciphertext), 64):
        block = binary_ciphertext[i:i+64]
        decrypted_block = decrypt_block(block, subkeys)
        plaintext += decrypted_block
    
    # Преобразование битовой строки в текст
    return ''.join(chr(int(plaintext[i:i+8], 2)) for i in range(0, len(plaintext), 8))

def read_encrypted_data(filename):
    """
    Читает зашифрованные данные из файла в кодировке UTF-16LE
    """
    full_path = os.path.expanduser(filename)
    
    print(f"Пытаемся прочитать файл: {full_path}")
    print(f"Файл существует: {os.path.exists(full_path)}")
    
    if not os.path.exists(full_path):
        print(f"Файл не найден: {full_path}")
        return None
        
    try:
        with open(full_path, 'rb') as file:  # Открываем в бинарном режиме
            raw_data = file.read()
            print(f"Прочитано байт: {len(raw_data)}")
            
            # Пробуем декодировать как UTF-16LE
            try:
                encrypted_data = raw_data.decode('utf-16le')
                print(f"Успешно декодировано как UTF-16LE, длина текста: {len(encrypted_data)}")
                return encrypted_data
            except UnicodeError:
                print("Ошибка при декодировании UTF-16LE, пробуем прочитать как есть")
                return raw_data
                
    except Exception as e:
        print(f"Ошибка при чтении файла: {str(e)}")
        return None

def prepare_key(key_string):
    key_bytes = key_string.encode('utf-16le')
    if len(key_bytes) < 8:
        key_bytes = key_bytes + b'\0' * (8 - len(key_bytes))
    elif len(key_bytes) > 8:
        key_bytes = key_bytes[:8]
    return key_bytes
def main():
    # Путь к файлу
    filename = "~/Desktop/MSU/7/cybersecurity/cryptography-algorithms-python/ciphers/16_enc.txt"
    
    # Читаем данные
    encrypted_data = read_encrypted_data(filename)
    
    print("\nСтатус данных:")
    print(f"Тип данных: {type(encrypted_data)}")
    if encrypted_data is not None:
        if isinstance(encrypted_data, bytes):
            print(f"Размер в байтах: {len(encrypted_data)}")
            # Выводим первые несколько байт для проверки
            print("Первые 20 байт:", encrypted_data[:20])
        else:
            print(f"Длина текста: {len(encrypted_data)}")
            print("Первые 20 символов:", repr(encrypted_data[:20]))
    
    if encrypted_data is None:
        print("Не удалось прочитать данные из файла")
        return
    
    # Подготавливаем ключ
    key = prepare_key("Хамидов Сиёвуш Ха")
    print(f"\nКлюч подготовлен, длина: {len(key)} байт")
    print("Ключ в байтах:", key)
    
    try:
        # Преобразуем ключ в битовую строку
        binary_key = ''.join(format(byte, '08b') for byte in key)
        print("Ключ в битах:", binary_key)
        print("Длина ключа в битах:", len(binary_key))
        
        # Если данные уже в байтах, используем их напрямую
        if isinstance(encrypted_data, bytes):
            ciphertext_bytes = encrypted_data
        else:
            # Иначе кодируем как UTF-16LE
            ciphertext_bytes = encrypted_data.encode('utf-16le')
        
        print(f"Данные подготовлены для расшифровки, размер: {len(ciphertext_bytes)} байт")
        
        # Расшифровываем
        decrypted_text = decrypt_des(ciphertext_bytes, binary_key)
        print("\nРасшифрованный текст:")
        print(decrypted_text)
        with open('file.txt', 'w') as f:
            f.write(decrypted_text)
        
    except Exception as e:
        print(f"\nПроизошла ошибка при расшифровке: {str(e)}")
        import traceback
        print("\nПолный стек ошибки:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
# # Пример использования для вашего конкретного случая:
# def decrypt_your_data(encrypted_data):
#     """
#     Функция для расшифровки вашего конкретного шифротекста
#     """
#     # Преобразуем ваш шифротекст в байты
#     # Это нужно адаптировать под формат ваших данных
#     ciphertext_bytes = bytes([ord(c) for c in encrypted_data])
    
#     # Предположим, что ключ известен (замените на правильный ключ)
#     key = b"SECRET!K"  # 8 байт
    
#     # Преобразуем ключ в битовую строку
#     binary_key = ''.join(format(byte, '08b') for byte in key)
    
#     # Расшифровываем
#     try:
#         decrypted_text = decrypt_des(ciphertext_bytes, binary_key)
#         return decrypted_text
#     except Exception as e:
#         return f"Ошибка расшифровки: {str(e)}"

# # Использование:
# encrypted_text = "ваш_шифротекст_здесь"
# result = decrypt_your_data(encrypted_text)
# print("Результат расшифровки:", result)

# print(decrypt_des("뽇狂땆톖坠킞킡圉톗⃂곐괄⨌Ⳑ訳ዢ肰߂ꑞ슷⿐鏐딒튐킝톅킬슻ⅿ᳐蹼矐뭓Ꮠ뽱̦㴅ැ鿂끷絯ℴ톖㫢股鰟톃㯢肔킿⡎♕ᠺ奿킭鱂໐돐飐郑鋐꫐觐闑迢肙ټ嬏킏톂톈킱䟑腚톀톗渁톇킏䃑鸫킔ᗐ뀕톏䫢肝濐軐髢蒢勐묟痢肹킻걊࿢肙톑킥킂ꈆ绑蓢肘⃂뇢肢໐靤鷢肝ᇐ蜯곐鷐뵟톆킌ϐ髐臐녕␈슶톆킜唬키㛑耻淐꿂걹⛐땄੃ࠍᗂ꧂ꛐ鰩鏢蒖湊킇말飐꧐蛢肚ௐ蛑萁키킣ᯑ觐Ꟑ驼킪킟슫킛㓑髐ꋂ곂ꯐ蛐鳂꧐苐陫킝먆ᣑ鯐ꍦ스愇멘ᨇ킇킁킧ੵ톃姑蓂ꛂꃐ뇢肢말뉳톛⭸킨⽤톚킠㋐蠽킼扯☑킣슮톈킞슰ᘄ킿킫톜绂ꀣ킸⯢肝ꀥ籑킗톃旐這킦懐鏑驸킼톄⛑舊톍⟑雐襞톊킰톜톎킇킧㇑蝦䥰绑铐딥㜅킘仂뙩킓킭⸶톏킘톉슘톜团肦킓䝂㟢肦킣䭫䋐謋킪䫑阛椙㫐믐镁슷㤝㷐裐雑驈톙⬘篐먤킙翐鼌㫢肦幧꘽Ɽ壐룐裑諂ꯐ鱅걩킄킕킢槂냢蒢킗䧐뫑萵킺෢肘㉾킚䋑虞࣑鿐ꃂꃐ괸෢肓ⓑ餩킗킹킭焂࣑鿐ꃂꃐ괸෢肓킇髂ꯐ茕Ὣᄶ킕슮槐따킄킜스廂뜯킓킵ዒ逷킆頝톛킾킫㫑鳐铐ꡀ킈킢驝킿킣킧穋浔톅㧂묇ࡰ톓ᇢ肰톒킵킃愯킽킄킮튐⟐蜈킷킮筥㯑頕バ듢肝킇拑蓢肰䣑蓐郐꽶渐슫ぞ珑訸呢ᩉ寑蟑蛑譈킐튑ᷢ蒢絪䇐酣罬킘໐驝슠၀㫢肢ḙ톜᭄ב雐裐띓䤑㔔┢슧톚⠣䃑鼆킽톌バ븊十킎㐇䄹냐荫䷑艁Ṇ緐꿢股톏䵒톌톛킏킌旐뭈킥乓슫錷飂ꤔ톒톖킛姑鈒톕䧐뱀킉킗⏑詑฽슠駐腖ጎ鐄킵킆톑烑锸Ⅎ丿仢肓阇킊嗐꫐韐깰偽톎슭ၡ습捌톙톃ⷑ觐齍㙤爷슫痐Ꟑ駐뷒郐襇킒ꉰ仐긪킸냐닑鸀狐뜌톇䱟⫐뵟空킄ฆ᝸㋢肦ਚ灦스톍킟슠킙Ⱏ톛巐묁ⷐꭴ슰ᗐ褟킑킋寑離肢톛슧ᕙ킇킃拢蒢⇂귢肢啻륞킈슮킪篐뤈슫킽⛐뱩슧Ӑ蕉ф筸籹弖킣슰슘旂뛂띫ꉱ튐킪駐葇킅슩톊맂뇐鵇슻ᯢ股킈킧ⴳ톚킁킅䀰킖⍡ⰳパ苂긹╣킉킇Ӣ肔㑟ᩆᨵ籭톉䅐킼습ꘐ킛슘킘킫鹌톆톄맂럐蓐끧톑킬톇੹킬톑ː륪䀂⠎瑖킭킠ꙥ톂킳킇篢肹ᩰ⧑蟐댘킼톑킥톓킬킆䕶櫐脹Ð裐酬킨旑賐뗐ꫢ肺킱냑闐꫐頧烐鸽킺톙䌌᳑輇ᴾᩳꉢ专키ݛ킐킆슘슬킃∧킔័鯐鑭킔拑釐룐뀛❻튑톎킥柢肢㛐럐觑胂頤⛐鰬톌旐臐굠킧킐슱톈킂筚ѕ䴠킫๞킩㷐끳䳑诐镾࿐菂ꃑ髂꧐蟐蝢킺킋톀킝阱킳Ⳑꄹ킮湈ţ䰗䬾⬄ǐ訴킑棐舾㐹킓키♏秂냐駐꣢芬昽㓢肘ꇐ鴝堤ᓑ腞킟톞㓐鼘킴튐ა걣끔硒톖킆ϐ輋奮킩ꇑ詶ꉩ漄䷢股ᓐ똥࿐븸킬ᛑ苑蓐謐䳑諢肚킃䍫ꋐꐴ䜚킑駐铐ꧢ肠톛㰿슻톆슬킼킖킓⃐髐ꝳ톓슱톔烐ꏐ뇂顃톞彲᩽ᤝ킽峑韢肦슷킝킶䋐뛐輙髑迂꧐ꃐ꧑訢ߐ踓㫐鳐ꌹ킣킖톛킈슘Ꙡ킟⋐댠৒逮킓࣐ꐒ", 'Хамидов'))
# print(decrypt_des("뽇狂땆톖坠킞킡圉톗⃂곐괄⨌Ⳑ訳ዢ肰߂ꑞ슷⿐鏐딒튐킝톅킬슻ⅿ᳐蹼矐뭓Ꮠ뽱̦㴅ැ鿂끷絯ℴ톖㫢股鰟톃㯢肔킿⡎♕ᠺ奿킭鱂໐돐飐郑鋐꫐觐闑迢肙ټ嬏킏톂톈킱䟑腚톀톗渁톇킏䃑鸫킔ᗐ뀕톏䫢肝濐軐髢蒢勐묟痢肹킻걊࿢肙톑킥킂ꈆ绑蓢肘⃂뇢肢໐靤鷢肝ᇐ蜯곐鷐뵟톆킌ϐ髐臐녕␈슶톆킜唬키㛑耻淐꿂걹⛐땄੃ࠍᗂ꧂ꛐ鰩鏢蒖湊킇말飐꧐蛢肚ௐ蛑萁키킣ᯑ觐Ꟑ驼킪킟슫킛㓑髐ꋂ곂ꯐ蛐鳂꧐苐陫킝먆ᣑ鯐ꍦ스愇멘ᨇ킇킁킧ੵ톃姑蓂ꛂꃐ뇢肢말뉳톛⭸킨⽤톚킠㋐蠽킼扯☑킣슮톈킞슰ᘄ킿킫톜绂ꀣ킸⯢肝ꀥ籑킗톃旐這킦懐鏑驸킼톄⛑舊톍⟑雐襞톊킰톜톎킇킧㇑蝦䥰绑铐딥㜅킘仂뙩킓킭⸶톏킘톉슘톜团肦킓䝂㟢肦킣䭫䋐謋킪䫑阛椙㫐믐镁슷㤝㷐裐雑驈톙⬘篐먤킙翐鼌㫢肦幧꘽Ɽ壐룐裑諂ꯐ鱅걩킄킕킢槂냢蒢킗䧐뫑萵킺෢肘㉾킚䋑虞࣑鿐ꃂꃐ괸෢肓ⓑ餩킗킹킭焂࣑鿐ꃂꃐ괸෢肓킇髂ꯐ茕Ὣᄶ킕슮槐따킄킜스廂뜯킓킵ዒ逷킆頝톛킾킫㫑鳐铐ꡀ킈킢驝킿킣킧穋浔톅㧂묇ࡰ톓ᇢ肰톒킵킃愯킽킄킮튐⟐蜈킷킮筥㯑頕バ듢肝킇拑蓢肰䣑蓐郐꽶渐슫ぞ珑訸呢ᩉ寑蟑蛑譈킐튑ᷢ蒢絪䇐酣罬킘໐驝슠၀㫢肢ḙ톜᭄ב雐裐띓䤑㔔┢슧톚⠣䃑鼆킽톌バ븊十킎㐇䄹냐荫䷑艁Ṇ緐꿢股톏䵒톌톛킏킌旐뭈킥乓슫錷飂ꤔ톒톖킛姑鈒톕䧐뱀킉킗⏑詑฽슠駐腖ጎ鐄킵킆톑烑锸Ⅎ丿仢肓阇킊嗐꫐韐깰偽톎슭ၡ습捌톙톃ⷑ觐齍㙤爷슫痐Ꟑ駐뷒郐襇킒ꉰ仐긪킸냐닑鸀狐뜌톇䱟⫐뵟空킄ฆ᝸㋢肦ਚ灦스톍킟슠킙Ⱏ톛巐묁ⷐꭴ슰ᗐ褟킑킋寑離肢톛슧ᕙ킇킃拢蒢⇂귢肢啻륞킈슮킪篐뤈슫킽⛐뱩슧Ӑ蕉ф筸籹弖킣슰슘旂뛂띫ꉱ튐킪駐葇킅슩톊맂뇐鵇슻ᯢ股킈킧ⴳ톚킁킅䀰킖⍡ⰳパ苂긹╣킉킇Ӣ肔㑟ᩆᨵ籭톉䅐킼습ꘐ킛슘킘킫鹌톆톄맂럐蓐끧톑킬톇੹킬톑ː륪䀂⠎瑖킭킠ꙥ톂킳킇篢肹ᩰ⧑蟐댘킼톑킥톓킬킆䕶櫐脹Ð裐酬킨旑賐뗐ꫢ肺킱냑闐꫐頧烐鸽킺톙䌌᳑輇ᴾᩳꉢ专키ݛ킐킆슘슬킃∧킔័鯐鑭킔拑釐룐뀛❻튑톎킥柢肢㛐럐觑胂頤⛐鰬톌旐臐굠킧킐슱톈킂筚ѕ䴠킫๞킩㷐끳䳑诐镾࿐菂ꃑ髂꧐蟐蝢킺킋톀킝阱킳Ⳑꄹ킮湈ţ䰗䬾⬄ǐ訴킑棐舾㐹킓키♏秂냐駐꣢芬昽㓢肘ꇐ鴝堤ᓑ腞킟톞㓐鼘킴튐ა걣끔硒톖킆ϐ輋奮킩ꇑ詶ꉩ漄䷢股ᓐ똥࿐븸킬ᛑ苑蓐謐䳑諢肚킃䍫ꋐꐴ䜚킑駐铐ꧢ肠톛㰿슻톆슬킼킖킓⃐髐ꝳ톓슱톔烐ꏐ뇂顃톞彲᩽ᤝ킽峑韢肦슷킝킶䋐뛐輙髑迂꧐ꃐ꧑訢ߐ踓㫐鳐ꌹ킣킖톛킈슘Ꙡ킟⋐댠৒逮킓࣐ꐒ", 'Сиёвуш'))
# print(decrypt_des("뽇狂땆톖坠킞킡圉톗⃂곐괄⨌Ⳑ訳ዢ肰߂ꑞ슷⿐鏐딒튐킝톅킬슻ⅿ᳐蹼矐뭓Ꮠ뽱̦㴅ැ鿂끷絯ℴ톖㫢股鰟톃㯢肔킿⡎♕ᠺ奿킭鱂໐돐飐郑鋐꫐觐闑迢肙ټ嬏킏톂톈킱䟑腚톀톗渁톇킏䃑鸫킔ᗐ뀕톏䫢肝濐軐髢蒢勐묟痢肹킻걊࿢肙톑킥킂ꈆ绑蓢肘⃂뇢肢໐靤鷢肝ᇐ蜯곐鷐뵟톆킌ϐ髐臐녕␈슶톆킜唬키㛑耻淐꿂걹⛐땄੃ࠍᗂ꧂ꛐ鰩鏢蒖湊킇말飐꧐蛢肚ௐ蛑萁키킣ᯑ觐Ꟑ驼킪킟슫킛㓑髐ꋂ곂ꯐ蛐鳂꧐苐陫킝먆ᣑ鯐ꍦ스愇멘ᨇ킇킁킧ੵ톃姑蓂ꛂꃐ뇢肢말뉳톛⭸킨⽤톚킠㋐蠽킼扯☑킣슮톈킞슰ᘄ킿킫톜绂ꀣ킸⯢肝ꀥ籑킗톃旐這킦懐鏑驸킼톄⛑舊톍⟑雐襞톊킰톜톎킇킧㇑蝦䥰绑铐딥㜅킘仂뙩킓킭⸶톏킘톉슘톜团肦킓䝂㟢肦킣䭫䋐謋킪䫑阛椙㫐믐镁슷㤝㷐裐雑驈톙⬘篐먤킙翐鼌㫢肦幧꘽Ɽ壐룐裑諂ꯐ鱅걩킄킕킢槂냢蒢킗䧐뫑萵킺෢肘㉾킚䋑虞࣑鿐ꃂꃐ괸෢肓ⓑ餩킗킹킭焂࣑鿐ꃂꃐ괸෢肓킇髂ꯐ茕Ὣᄶ킕슮槐따킄킜스廂뜯킓킵ዒ逷킆頝톛킾킫㫑鳐铐ꡀ킈킢驝킿킣킧穋浔톅㧂묇ࡰ톓ᇢ肰톒킵킃愯킽킄킮튐⟐蜈킷킮筥㯑頕バ듢肝킇拑蓢肰䣑蓐郐꽶渐슫ぞ珑訸呢ᩉ寑蟑蛑譈킐튑ᷢ蒢絪䇐酣罬킘໐驝슠၀㫢肢ḙ톜᭄ב雐裐띓䤑㔔┢슧톚⠣䃑鼆킽톌バ븊十킎㐇䄹냐荫䷑艁Ṇ緐꿢股톏䵒톌톛킏킌旐뭈킥乓슫錷飂ꤔ톒톖킛姑鈒톕䧐뱀킉킗⏑詑฽슠駐腖ጎ鐄킵킆톑烑锸Ⅎ丿仢肓阇킊嗐꫐韐깰偽톎슭ၡ습捌톙톃ⷑ觐齍㙤爷슫痐Ꟑ駐뷒郐襇킒ꉰ仐긪킸냐닑鸀狐뜌톇䱟⫐뵟空킄ฆ᝸㋢肦ਚ灦스톍킟슠킙Ⱏ톛巐묁ⷐꭴ슰ᗐ褟킑킋寑離肢톛슧ᕙ킇킃拢蒢⇂귢肢啻륞킈슮킪篐뤈슫킽⛐뱩슧Ӑ蕉ф筸籹弖킣슰슘旂뛂띫ꉱ튐킪駐葇킅슩톊맂뇐鵇슻ᯢ股킈킧ⴳ톚킁킅䀰킖⍡ⰳパ苂긹╣킉킇Ӣ肔㑟ᩆᨵ籭톉䅐킼습ꘐ킛슘킘킫鹌톆톄맂럐蓐끧톑킬톇੹킬톑ː륪䀂⠎瑖킭킠ꙥ톂킳킇篢肹ᩰ⧑蟐댘킼톑킥톓킬킆䕶櫐脹Ð裐酬킨旑賐뗐ꫢ肺킱냑闐꫐頧烐鸽킺톙䌌᳑輇ᴾᩳꉢ专키ݛ킐킆슘슬킃∧킔័鯐鑭킔拑釐룐뀛❻튑톎킥柢肢㛐럐觑胂頤⛐鰬톌旐臐굠킧킐슱톈킂筚ѕ䴠킫๞킩㷐끳䳑诐镾࿐菂ꃑ髂꧐蟐蝢킺킋톀킝阱킳Ⳑꄹ킮湈ţ䰗䬾⬄ǐ訴킑棐舾㐹킓키♏秂냐駐꣢芬昽㓢肘ꇐ鴝堤ᓑ腞킟톞㓐鼘킴튐ა걣끔硒톖킆ϐ輋奮킩ꇑ詶ꉩ漄䷢股ᓐ똥࿐븸킬ᛑ苑蓐謐䳑諢肚킃䍫ꋐꐴ䜚킑駐铐ꧢ肠톛㰿슻톆슬킼킖킓⃐髐ꝳ톓슱톔烐ꏐ뇂顃톞彲᩽ᤝ킽峑韢肦슷킝킶䋐뛐輙髑迂꧐ꃐ꧑訢ߐ踓㫐鳐ꌹ킣킖톛킈슘Ꙡ킟⋐댠৒逮킓࣐ꐒ", 'Халифабобоевич'))



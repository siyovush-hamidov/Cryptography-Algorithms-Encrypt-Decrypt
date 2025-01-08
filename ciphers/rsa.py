from sympy import mod_inverse, gcd
from random import randint

class RSACipher:
    @staticmethod
    def encrypt_ascii(message: str, characters: str, p: int, q: int):
        # lower_bound = 2
        # upper_bound = 2 ** 10 - 1
        # Генерация случайных простых чисел p и q
        # p = randprime(lower_bound, upper_bound)
        # q = randprime(lower_bound, upper_bound)
        # Вычисление модуля n и функции Эйлера phi(n)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        # Выбор e и вычисление d
        while True:
            e = randint(2, phi_n - 1)
            if gcd(e, phi_n) == 1:  # Проверка, что e взаимно просто с phi_n
                break
        d = mod_inverse(e, phi_n)

        # Печать ключей (опционально)
        print(f"PUBLIC KEY:\ne={e}\nPUBLIC KEY:\nn={n}")
        print(f"PRIVATE KEY:\nd={d}\nPRIVATE KEY:\nn={n}")

        # Убедимся, что все символы сообщения входят в алфавит
        if any(char not in characters for char in message):
            raise ValueError(
                "Message contains characters not in the allowed alphabet.")

        # Шифрование сообщения
        # Преобразование символов в их индексы в алфавите
        message_as_int = [characters.index(char) for char in message]
        # Шифрование по формуле m^e mod n
        encrypted_message = [pow(m, e, n) for m in message_as_int]
        # Возврат зашифрованного сообщения и закрытого ключа
        return encrypted_message, d, n

    @staticmethod
    def decrypt_ascii(encrypted_message: str, d: int, n: int, characters: str):
        # Расшифровка каждого числа в сообщение
        encrypted_numbers = [
            int(num.strip())  # Убираем пробелы и преобразуем в int
            for num in encrypted_message.strip('[]').split(',')
            if num.strip().isdigit()  # Проверяем, что это число
        ]
        decrypted_message = [characters[pow(c, d, n)]
                             for c in encrypted_numbers]
        return ''.join(decrypted_message)

    @staticmethod
    def encrypt_unicode(message: str, p, q):
        lower_bound = 2 ** (1024 - 1)
        upper_bound = 2 ** 1024 - 1
        # Вычисление модуля n и функции Эйлера phi(n)
        n = p * q
        phi_n = (p - 1) * (q - 1)
        # Выбор e и вычисление d
        while True:
            e = randint(2, phi_n - 1)
            if gcd(e, phi_n) == 1:  # Проверка, что e взаимно просто с phi_n
                break
        d = mod_inverse(e, phi_n)

        # Печать ключей (опционально)
        print(f"Public key: (e={e}, n={n})")
        print(f"Private key: (d={d}, n={n})")

        # Шифрование сообщения
        # Преобразование символов в их коды
        message_as_int = [ord(char) for char in message]
        # Шифрование по формуле m^e mod n
        encrypted_message = [pow(m, e, n) for m in message_as_int]
        # Возврат зашифрованного сообщения и закрытого ключа
        return encrypted_message, (d, n)

    def find_d_and_e(p, q):
        n = p * q
        fi_n = (p - 1) * (q - 1)

        d = n - 1
        i = 2

        while i <= fi_n:
            if d % i == 0:
                d -= 1
                i = 2
                continue
            i += 1

        e = 10
        while (e * d) % fi_n != 1:
            e += 1

        return d, e, n, fi_n


    @staticmethod
    def decrypt_unicode(encrypted_message, p, q):
        try:
            n = p * q
            fi_n = (p - 1) * (q - 1)

            d = n - 1
            i = 2

            while i <= fi_n:
                if d % i == 0:
                    d -= 1
                    i = 2
                    continue
                i += 1

            e = 10
            while (e * d) % fi_n != 1:
                e += 1
                n = p * q
                fi_n = (p - 1) * (q - 1)
        except Exception as e:
            return f"Ошибка при вычислении n или φ(n): {e} или Не удалось найти подходящие значения e и d"
        
        # try:
        #     # Поиск e и вычисление d
        #     e, d = None, None
        #     for candidate_e in range(10, fi_n):
        #         if gcd(candidate_e, fi_n) == 1:
        #             e = candidate_e
        #             d = mod_inverse(e, fi_n)
        #             break
        #     if e is None or d is None:
                
        # except Exception as e:
        #     return f"Ошибка при вычислении e и d: {e}"
        
        decrypted_message = ""
        for char in encrypted_message:
            try:
                c = ord(char) - 32  # Убираем сдвиг до 32-го символа
                decrypted_char = chr((pow(c, d, n) % (0x10FFFF - 32)) + 32)  # Расшифровка и возврат в диапазон Unicode
                decrypted_message += decrypted_char
                # c = ord(char)  # Преобразуем символ в его числовое представление
                # decrypted_char = chr(pow(c, d, n))  # Расшифровка символа
                # decrypted_message += decrypted_char
            except Exception as e:
                return f"Ошибка при расшифровке символа '{char}': {e}"
        
        return n, fi_n, e, d, decrypted_message
    
    # def decrypt_unicode(encrypted_message, p, q):
    #     n = p * q
    #     fi_n = (p - 1) * (q - 1)
        
    #     # Поиск e и вычисление d
    #     e = None
    #     d = None
    #     for candidate_e in range(2, fi_n):
    #         if gcd(candidate_e, fi_n) == 1:
    #             e = candidate_e
    #             d = mod_inverse(e, fi_n)
    #             break
        
    #     if e is None or d is None:
    #         return ''.join("Не удалось найти подходящие значения e и d")
    #         # raise ValueError("Не удалось найти подходящие значения e и d")
        
    #     # Расшифровка сообщения
    #     decrypted_message = ""
    #     for char in encrypted_message:
    #         c = ord(char)  # Преобразуем символ в его числовое представление
    #         decrypted_char = chr(pow(c, d, n))  # Расшифровка символа
    #         decrypted_message += decrypted_char
        
    #     return ''.join(decrypted_message)


# # Пример использования
# rsa = RSACipher()
# message = "Пример текста из доступного алфавита!"  # Сообщение только из characters
# characters = "".join(chr(i).encode('latin1').decode('cp1251', errors='replace') for i in range(32, 256))
# # Шифрование
# encrypted_message, d, n = rsa.encrypt_ascii(message, characters, 17, 19)
# print("Encrypted Message:", encrypted_message, d, n)

# # Расшифровка
# decrypted_message = rsa.decrypt_ascii(encrypted_message, d, n, characters)
# print("Decrypted Message:", decrypted_message)

# # Проверка
# assert message == decrypted_message, "Ошибка: сообщение не совпадает!"

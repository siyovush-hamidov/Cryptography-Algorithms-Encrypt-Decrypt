from sympy import randprime, mod_inverse, gcd
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
        # Генерация случайных простых чисел p и q
        p = randprime(lower_bound, upper_bound)
        q = randprime(lower_bound, upper_bound)
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

    @staticmethod
    def decrypt_unicode(encrypted_message, private_key, p, q):
        d, n = private_key
        # Расшифровка каждого числа в сообщение
        decrypted_message = [chr(pow(c, d, n)) for c in encrypted_message]
        return ''.join(decrypted_message)


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

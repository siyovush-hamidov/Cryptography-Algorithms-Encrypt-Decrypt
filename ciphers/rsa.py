from sympy import randprime, mod_inverse, gcd
from random import randint


class RSACipher:

    @staticmethod
    def encrypt_unicode(message: str):
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
    def decrypt_unicode(encrypted_message, private_key):
        d, n = private_key
        # Расшифровка каждого числа в сообщение
        decrypted_message = [chr(pow(c, d, n)) for c in encrypted_message]
        return ''.join(decrypted_message)

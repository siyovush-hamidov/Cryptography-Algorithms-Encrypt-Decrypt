from sympy import mod_inverse, gcd
from random import randint

class RSACipher:
    def find_d_and_e(p, q):
        n = p * q
        m = (p - 1) * (q - 1)
        d = n - 1
        i = 2
        while i <= m:
            d_mod_i = d % i
            if d_mod_i == 0:
                d -= 1
                i = 2
                continue
            i += 1

        e = 10
        while (e * d) % m != 1:
            e += 1
        
        return {'d': d, 'e': e, 'n': n, 'm': m}

    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True

    @staticmethod    
    def decrypt_text_from_unicode(encrypted, d, n):
        decrypted = ''
        for char in encrypted:
            try:
                # c = ord(char) - 32  # Убираем сдвиг до 32-го символа
                # decrypted_char = chr((pow(c, d, n) % (0x10FFFF - 32)) + 32)  # Расшифровка и возврат в диапазон Unicode
                # decrypted += decrypted_char
                char_code = ord(char)
                decrypted_char = pow(char_code, d, n)
                decrypted += chr(decrypted_char)
            except Exception as e:
                return f"Ошибка при расшифровке символа '{char}': {e}"
        return decrypted

    @staticmethod
    def decrypt(encrypted_message, p, q):
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
    
    # НИЖЕ НАСТОЯЩИЙ RSA
    # def gcd(a, b):
    #     while b:
    #         a, b = b, a % b
    #     return a

    # def mod_inverse(e, phi):
    #     def extended_gcd(a, b):
    #         if a == 0:
    #             return b, 0, 1
    #         gcd, x1, y1 = extended_gcd(b % a, a)
    #         x = y1 - (b // a) * x1
    #         y = x1
    #         return gcd, x, y
        
    #     _, x, _ = extended_gcd(e, phi)
    #     return x % phi

    # def find_d_and_e(p, q):
    #     n = p * q
    #     phi = (p - 1) * (q - 1)
        
    #     # Выбираем e: 1 < e < phi и e взаимно просто с phi
    #     e = 65537  # Стандартное значение для e (2^16 + 1)
    #     while e < phi:
    #         if gcd(e, phi) == 1:
    #             break
    #         e += 2
        
    #     # Вычисляем d: (d * e) mod phi = 1
    #     d = mod_inverse(e, phi)
        
    #     return {'d': d, 'e': e, 'n': n, 'm': phi}
from sympy import mod_inverse, gcd, prime
from random import randint

class RSACipher:
    @staticmethod
    def calculate_d_and_e(p, q):
        n = p * q
        phi = (p - 1) * (q - 1)
        
        i = 2
        d = n - 1
        while i <= phi:
            if d % i == 0 and phi % i == 0:
                d -= 1
                i = 2
                continue
            i += 1

        e = 10
        while (e * d) % phi != 1:
            e += 1
        
        return {'d': d, 'e': e, 'n': n, 'm': phi}

    @staticmethod
    def encrypt(message, p, q, d):
        n = p * q
        phi = (p - 1) * (q - 1)
        e = 10
        while (e * d) % phi != 1:
            e += 1
        encrypted = []
        try:
            for char in message:
                char_code = ord(char)
                encrypted_code = pow(char_code, e, n)
                encrypted.append(chr(encrypted_code % 65536))
        except Exception as e:
            return f"Ошибка при шифровании: {e}"
        return ''.join(encrypted).replace('\u200b', '')

    @staticmethod
    def decrypt(encrypted_message, p, q):
        try:
            n = p * q
            fi_n = (p - 1) * (q - 1)
        except Exception as e:
            return f"Ошибка при вычислении n или φ(n): {e}"

        decrypted_messages = []
        three_chars = ""  # Initialize the variable to hold the first 5 characters
        for ch in encrypted_message:
            three_chars += ch
            if len(three_chars) > 2:
                break

        for d in range(10, n + 1):
            valid_chars_count = sum(1 for c in three_chars if 1040 <= pow(ord(c), d, n) <= 1103)
            if valid_chars_count >= 2:  # If 5 or more characters satisfy the condition
                print(f"p = {p} | q = {q} | d = {d}")

                decrypted_message = ""
                for char in encrypted_message:
                    try:
                        decrypted_message += chr(pow(ord(char), d, n))  # Decrypt each character
                    except Exception as e:
                        return f"Ошибка при расшифровке символа '{char}': {e}"

                decrypted_messages.append(decrypted_message + '\n' + f"d = {d}" + '\n')

        return decrypted_messages

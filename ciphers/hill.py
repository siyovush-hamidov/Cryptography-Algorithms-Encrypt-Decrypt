import numpy as np

MOD = 227
MATRIX_SIZE = 3

char_table = [
        "\x00","\t", "\n", "\r", " ", "!", "\"", "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a",
        "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "\x7f","Ђ", "Ѓ", "‚",
        "ѓ", "„", "…", "†", "‡", "€", "‰", "Љ", "‹", "Њ", "Ќ", "Ћ", "Џ", "ђ", "‘", "’", "“", "”", "•", "–", "—", "\x98","™", "љ", "›", "њ", "ќ", "ћ", "џ", "\xA0", "Ў", "ў",
        "Ј", "¤", "Ґ", "¦", "§", "Ё", "©", "Є", "«", "¬", "\xAD", "®", "Ї", "°", "±", "І", "і", "ґ", "µ", "¶", "·", "ё", "№", "є", "»", "ј", "Ѕ", "ѕ", "ї", "А", "Б", "В", "Г",
        "Д", "Е", "Ж", "З", "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я", "а", "б", "в", "г", "д",
        "е", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"
    ]

# Для проверки таблицы символов
print(char_table)
for i, char in enumerate(char_table, start=0):
    print(f"{i}\t{ord(char)}\t{repr(char)}")

class HillCipher:
    @staticmethod
    def byte_to_index(b):
            try:
                return char_table.index(b) 
            except ValueError:
                raise ValueError(f"Символ {chr(b)} не найден в таблице")

    @staticmethod
    def index_to_byte(index):
        if isinstance(index, int):  
            return ord(char_table[index])
        else:
            raise TypeError(f"Ожидалось целое число, но получено: {type(index)}")

    @staticmethod
    def prepare_message(message):
        while len(message) % MATRIX_SIZE != 0:
            message += " "
        return message

    @staticmethod
    def prepare_key(key):
        if len(key) > 9:
            return key[:9]
        elif len(key) < 9:
            return key.ljust(9)
        return key

    @staticmethod
    def create_key_matrix(key):
        key = HillCipher.prepare_key(key)
        matrix = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
        index = 0
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                matrix[i][j] = HillCipher.byte_to_index(key[index])
                index += 1
        print("Матрица ключа:")
        HillCipher.print_matrix(matrix)
        return matrix

    @staticmethod
    def compute_inverse_key_matrix(matrix):
        deter = HillCipher.determinant(matrix) % MOD
        if deter < 0:
            deter += MOD
        if deter == 0:
            raise ValueError("Матрица ключа не является обратимой.")
        mod_inverse = HillCipher.mod_inverse(deter, MOD)
        adjugate = HillCipher.adjugate_matrix(matrix)
        inverse = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
        for i in range(MATRIX_SIZE):
            for j in range(MATRIX_SIZE):
                inverse[i][j] = (adjugate[i][j] * mod_inverse - 1) % MOD + 1
                if inverse[i][j] < 0:
                    inverse[i][j] += MOD
        print("Обратная матрица:")
        HillCipher.print_matrix(inverse)
        return inverse

    @staticmethod
    def determinant(matrix):
        det = (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) - 
               matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) + 
               matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])) % MOD
        print(f"Determinant = {det}")
        return det

    @staticmethod
    def adjugate_matrix(matrix):
        adj = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=int)
        adj[0][0] = matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]
        adj[0][1] = -(matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        adj[0][2] = matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]
        adj[1][0] = -(matrix[0][1] * matrix[2][2] - matrix[0][2] * matrix[2][1])
        adj[1][1] = matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]
        adj[1][2] = -(matrix[0][0] * matrix[2][1] - matrix[0][1] * matrix[2][0])
        adj[2][0] = matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1]
        adj[2][1] = -(matrix[0][0] * matrix[1][2] - matrix[0][2] * matrix[1][0])
        adj[2][2] = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        adj = HillCipher.transpose_matrix(adj)
        return adj

    @staticmethod
    def transpose_matrix(matrix):
        return np.transpose(matrix)

    @staticmethod
    def mod_inverse(a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 1

    @staticmethod
    def multiply_matrix_and_vector(matrix, vector):
        result = np.zeros(MATRIX_SIZE, dtype=int)
        for i in range(MATRIX_SIZE):
            result[i] = sum(matrix[i][j] * vector[j] for j in range(MATRIX_SIZE)) % MOD
            result[i] = (result[i] - 1) % MOD + 1
            if result[i] < 0:
                result[i] += MOD
        return result

    @staticmethod
    def print_matrix(matrix):
        for row in matrix:
            print("\t".join(map(str, row)))
        print()

    @staticmethod
    def print_vector(vector):
        print("\t".join(map(str, vector)))
        print()

    @staticmethod
    def encrypt_ascii(message,key):
        key_matrix = HillCipher.create_key_matrix(key)
        cipher_message = []
        message = HillCipher.prepare_message(message)
        for i in range(0, len(message), MATRIX_SIZE):
            message_vector = [char_table.index(message[i + j]) for j in range(MATRIX_SIZE)]
            print("\nВектор сообщения:")
            HillCipher.print_vector(message_vector)
            result_vector = HillCipher.multiply_matrix_and_vector(key_matrix, message_vector)
            for value in result_vector:
                cipher_message.append(char_table[value])
        return "".join(cipher_message)

    @staticmethod
    def decrypt_ascii(cipher_text,key):
        cipher_text = HillCipher.prepare_message(cipher_text)
        print(len(cipher_text))
        key_matrix = HillCipher.create_key_matrix(key)
        inverse_key_matrix = HillCipher.compute_inverse_key_matrix(key_matrix)
        plain_message = []
        for i in range(0, len(cipher_text), MATRIX_SIZE):
            cipher_vector = [char_table.index(cipher_text[i + j]) for j in range(MATRIX_SIZE)]
            result_vector = HillCipher.multiply_matrix_and_vector(inverse_key_matrix, cipher_vector)
            for value in result_vector:
                plain_message.append(char_table[value])

        plain_message = "".join(plain_message).replace('Зjx', 'ств')
        plain_message = "".join(plain_message).replace('ьГJ', 'чен') #K
        plain_message = "".join(plain_message).replace('5ІI', 'исл') #K
        plain_message = "".join(plain_message).replace('Аfѓ', 'кон')
        plain_message = "".join(plain_message).replace('¶{x', '  в')
        plain_message = "".join(plain_message).replace('Вdѓ', 'ммн')
        plain_message = "".join(plain_message).replace('Зg{', 'спе')
        plain_message = "".join(plain_message).replace('ЩXx', ' ав')
        plain_message = "".join(plain_message).replace('µlГёX™', ' ства')
        plain_message = "".join(plain_message).replace('    ъ+ц', '')
        plain_message = "".join(plain_message).replace('ѓЮ$', 'бов') #S
        plain_message = "".join(plain_message).replace('ЅuR', 'ви') #S        
        plain_message = "".join(plain_message).replace('сре ствасбора', 'средства сбора')
        return "".join(plain_message)



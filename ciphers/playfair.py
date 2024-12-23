class PlayfairCipher:
    def __init__(self, keyword: str):
        self.key = keyword
        self.matrix = self.generate_matrix(self.key)

    def generate_matrix(self, keyword: str):
        """
        Создаёт матрицу 14x16 на основе ключа:
        1. Объединяет ключ с остальными символами.
        2. Удаляет дублирующиеся символы, сохраняя порядок.
        """
        # Создаём полный набор символов от пробела (ASCII 32) до 'я'
        characters = "".join(chr(i).encode('latin1').decode('cp1251', errors='replace') for i in range(32, 256))
        # Объединяем ключ и полный набор символов, удаляем дубликаты
        full_set = "".join(dict.fromkeys(keyword + characters))
        # Разбиваем на строки по 16 символов
        matrix = [full_set[i:i + 16] for i in range(0, len(full_set), 16)]
        self.print_matrix(matrix)
        return matrix

    def print_matrix(self, matrix):
        """
        Выводит матрицу ключа в удобочитаемом формате.
        """
        print("Playfair Cipher Key Matrix:")
        for row in matrix:
            print(" ".join(row))
        print()

    def find_position(self, char):
        """
        Находит позицию символа в матрице. Возвращает (строка, столбец).
        """
        for row_index, row in enumerate(self.matrix):
            if char in row:
                return row_index, row.index(char)
        return None

    def process_text(self, text):
        """
        Подготавливает текст для шифрования:
        1. Разбивает текст на биграммы. Если буквы в биграмме одинаковые, вторая заменяется на 'x'.
        2. Добавляет 'x', если текст имеет нечётное количество символов.
        """
        bigrams = []
        i = 0
        while i < len(text):
            char1 = text[i]
            if i + 1 < len(text) and text[i + 1] != char1:
                char2 = text[i + 1]
                i += 2
            else:
                char2 = "x"  # Добавляем 'x' для заполнения
                i += 1
            bigrams.append((char1, char2))
        return bigrams

    def encrypt_ascii(self, text: str, keyword: str) -> str:
        """
        Шифрует текст по следующим правилам:
        1. Если две буквы находятся в одной строке матрицы, заменяются на следующие справа.
        2. Если в одном столбце, заменяются на буквы ниже.
        3. Если образуют прямоугольник, заменяются на противоположные углы.
        """
        self.key = keyword
        self.matrix = self.generate_matrix(keyword)
        # Нужно сгенерировать таблицу
        bigrams = self.process_text(text)
        encrypted_text = []

        for char1, char2 in bigrams:
            row1, col1 = self.find_position(char1)
            row2, col2 = self.find_position(char2)

            if row1 == row2:  # В одной строке
                encrypted_text.append(self.matrix[row1][(col1 + 1) % 16])
                encrypted_text.append(self.matrix[row2][(col2 + 1) % 16])
            elif col1 == col2:  # В одном столбце
                encrypted_text.append(self.matrix[(row1 + 1) % 14][col1])
                encrypted_text.append(self.matrix[(row2 + 1) % 14][col2])
            else:  # Прямоугольник
                encrypted_text.append(self.matrix[row1][col2])
                encrypted_text.append(self.matrix[row2][col1])

        return "".join(encrypted_text)

    def decrypt_ascii(self, text: str, keyword: str) -> str:
        """
        Расшифровывает текст по следующим правилам:
        1. Если две буквы находятся в одной строке матрицы, заменяются на предыдущие слева.
        2. Если в одном столбце, заменяются на буквы выше.
        3. Если образуют прямоугольник, заменяются на противоположные углы.
        """
        self.key = keyword
        self.matrix = self.generate_matrix(keyword)
        bigrams = [(text[i], text[i + 1]) for i in range(0, len(text), 2)]
        decrypted_text = []

        for char1, char2 in bigrams:
            row1, col1 = self.find_position(char1)
            row2, col2 = self.find_position(char2)

            if row1 == row2:  # В одной строке
                decrypted_text.append(self.matrix[row1][(col1 - 1) % 14])
                decrypted_text.append(self.matrix[row2][(col2 - 1) % 14])
            elif col1 == col2:  # В одном столбце
                decrypted_text.append(self.matrix[(row1 - 1) % 16][col1])
                decrypted_text.append(self.matrix[(row2 - 1) % 16][col2])
            else:  # Прямоугольник
                decrypted_text.append(self.matrix[row1][col2])
                decrypted_text.append(self.matrix[row2][col1])

        return "".join(decrypted_text)

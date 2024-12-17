import string


class PlayfairCipher:
    def __init__(self, key: str):
        """
        Инициализация шифра. Генерируется ключевая матрица 5x5 на основе введённого ключа.
        """
        self.key = key
        self.matrix = self._generate_matrix()

    def _generate_matrix(self):
        """
        Создаёт матрицу 5x5 на основе ключа:
        1. Удаляет пробелы и объединяет ключ с алфавитом.
        2. Исключает букву 'j' из алфавита.
        3. Удаляет дублирующиеся символы, оставляя порядок появления.
        """
        alphabet = string.ascii_lowercase.replace("j", "")  # Алфавит без 'j'
        key = "".join(dict.fromkeys(self.key.lower().replace(" ", "") + alphabet))  # Формируем строку
        matrix = [key[i:i+5] for i in range(0, 25, 5)]  # Разбиваем на строки матрицы
        self._print_matrix(matrix)  # Выводим матрицу для проверки
        return matrix

    def _print_matrix(self, matrix):
        """
        Выводит матрицу ключа в удобочитаемом формате.
        """
        print("Playfair Cipher Key Matrix:")
        for row in matrix:
            print(" ".join(row))
        print()

    def _find_position(self, char):
        """
        Находит позицию символа в матрице. Возвращает (строка, столбец).
        """
        for row_index, row in enumerate(self.matrix):
            if char in row:
                return row_index, row.index(char)
        return None

    def _process_text(self, text):
        """
        Подготавливает текст для шифрования:
        1. Преобразует в нижний регистр и заменяет 'j' на 'i'.
        2. Удаляет неалфавитные символы.
        3. Разбивает текст на биграммы. Если буквы в биграмме одинаковые, вторая заменяется на 'x'.
        4. Добавляет 'x', если текст имеет нечётное количество символов.
        """
        text = text.lower().replace("j", "i")
        text = "".join(filter(str.isalpha, text))  # Удаляем лишние символы

        bigrams = []
        i = 0
        while i < len(text):
            char1 = text[i]
            if i + 1 < len(text) and text[i + 1] != char1:
                char2 = text[i + 1]
                i += 2
            else:
                char2 = "x"  # Добавляем "x" для заполнения
                i += 1
            bigrams.append((char1, char2))
        return bigrams

    def playfair_encode(self, text: str) -> str:
        """
        Шифрует текст по следующим правилам:
        1. Если две буквы находятся в одной строке матрицы, заменяются на следующие справа.
        2. Если в одном столбце, заменяются на буквы ниже.
        3. Если образуют прямоугольник, заменяются на противоположные углы.
        """
        bigrams = self._process_text(text)
        encrypted_text = []

        for char1, char2 in bigrams:
            row1, col1 = self._find_position(char1)
            row2, col2 = self._find_position(char2)

            if row1 == row2:  # В одной строке
                encrypted_text.append(self.matrix[row1][(col1 + 1) % 5])
                encrypted_text.append(self.matrix[row2][(col2 + 1) % 5])
            elif col1 == col2:  # В одном столбце
                encrypted_text.append(self.matrix[(row1 + 1) % 5][col1])
                encrypted_text.append(self.matrix[(row2 + 1) % 5][col2])
            else:  # Прямоугольник
                encrypted_text.append(self.matrix[row1][col2])
                encrypted_text.append(self.matrix[row2][col1])

        return "".join(encrypted_text)

    def playfair_decode(self, text: str) -> str:
        """
        Расшифровывает текст по следующим правилам:
        1. Если две буквы находятся в одной строке матрицы, заменяются на предыдущие слева.
        2. Если в одном столбце, заменяются на буквы выше.
        3. Если образуют прямоугольник, заменяются на противоположные углы.
        """
        bigrams = [(text[i], text[i + 1]) for i in range(0, len(text), 2)]
        decrypted_text = []

        for char1, char2 in bigrams:
            row1, col1 = self._find_position(char1)
            row2, col2 = self._find_position(char2)

            if row1 == row2:  # В одной строке
                decrypted_text.append(self.matrix[row1][(col1 - 1) % 5])
                decrypted_text.append(self.matrix[row2][(col2 - 1) % 5])
            elif col1 == col2:  # В одном столбце
                decrypted_text.append(self.matrix[(row1 - 1) % 5][col1])
                decrypted_text.append(self.matrix[(row2 - 1) % 5][col2])
            else:  # Прямоугольник
                decrypted_text.append(self.matrix[row1][col2])
                decrypted_text.append(self.matrix[row2][col1])

        return "".join(decrypted_text)
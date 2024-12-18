# import string


# class PlayfairCipher:
#     def __init__(self, key: str):
#         """
#         Инициализация шифра. Генерируется ключевая матрица 5x5 на основе введённого ключа.
#         """
#         self.key = key
#         self.matrix = self._generate_matrix()

#     def _generate_matrix(self):
#         """
#         Создаёт матрицу 5x5 на основе ключа:
#         1. Удаляет пробелы и объединяет ключ с алфавитом.
#         2. Исключает букву 'j' из алфавита.
#         3. Удаляет дублирующиеся символы, оставляя порядок появления.
#         """
#         alphabet = string.ascii_lowercase.replace("j", "")  # Алфавит без 'j'
#         key = "".join(dict.fromkeys(self.key.lower().replace(" ", "") + alphabet))  # Формируем строку
#         matrix = [key[i:i+5] for i in range(0, 25, 5)]  # Разбиваем на строки матрицы
#         self._print_matrix(matrix)  # Выводим матрицу для проверки
#         return matrix

#     def _print_matrix(self, matrix):
#         """
#         Выводит матрицу ключа в удобочитаемом формате.
#         """
#         print("Playfair Cipher Key Matrix:")
#         for row in matrix:
#             print(" ".join(row))
#         print()

#     def _find_position(self, char):
#         """
#         Находит позицию символа в матрице. Возвращает (строка, столбец).
#         """
#         for row_index, row in enumerate(self.matrix):
#             if char in row:
#                 return row_index, row.index(char)
#         return None

#     def _process_text(self, text):
#         """
#         Подготавливает текст для шифрования:
#         1. Преобразует в нижний регистр и заменяет 'j' на 'i'.
#         2. Удаляет неалфавитные символы.
#         3. Разбивает текст на биграммы. Если буквы в биграмме одинаковые, вторая заменяется на 'x'.
#         4. Добавляет 'x', если текст имеет нечётное количество символов.
#         """
#         text = text.lower().replace("j", "i")
#         text = "".join(filter(str.isalpha, text))  # Удаляем лишние символы

#         bigrams = []
#         i = 0
#         while i < len(text):
#             char1 = text[i]
#             if i + 1 < len(text) and text[i + 1] != char1:
#                 char2 = text[i + 1]
#                 i += 2
#             else:
#                 char2 = "x"  # Добавляем "x" для заполнения
#                 i += 1
#             bigrams.append((char1, char2))
#         return bigrams

#     def playfair_encode(self, text: str) -> str:
#         """
#         Шифрует текст по следующим правилам:
#         1. Если две буквы находятся в одной строке матрицы, заменяются на следующие справа.
#         2. Если в одном столбце, заменяются на буквы ниже.
#         3. Если образуют прямоугольник, заменяются на противоположные углы.
#         """
#         bigrams = self._process_text(text)
#         encrypted_text = []

#         for char1, char2 in bigrams:
#             row1, col1 = self._find_position(char1)
#             row2, col2 = self._find_position(char2)

#             if row1 == row2:  # В одной строке
#                 encrypted_text.append(self.matrix[row1][(col1 + 1) % 5])
#                 encrypted_text.append(self.matrix[row2][(col2 + 1) % 5])
#             elif col1 == col2:  # В одном столбце
#                 encrypted_text.append(self.matrix[(row1 + 1) % 5][col1])
#                 encrypted_text.append(self.matrix[(row2 + 1) % 5][col2])
#             else:  # Прямоугольник
#                 encrypted_text.append(self.matrix[row1][col2])
#                 encrypted_text.append(self.matrix[row2][col1])

#         return "".join(encrypted_text)

#     def playfair_decode(self, text: str) -> str:
#         """
#         Расшифровывает текст по следующим правилам:
#         1. Если две буквы находятся в одной строке матрицы, заменяются на предыдущие слева.
#         2. Если в одном столбце, заменяются на буквы выше.
#         3. Если образуют прямоугольник, заменяются на противоположные углы.
#         """
#         bigrams = [(text[i], text[i + 1]) for i in range(0, len(text), 2)]
#         decrypted_text = []

#         for char1, char2 in bigrams:
#             row1, col1 = self._find_position(char1)
#             row2, col2 = self._find_position(char2)

#             if row1 == row2:  # В одной строке
#                 decrypted_text.append(self.matrix[row1][(col1 - 1) % 5])
#                 decrypted_text.append(self.matrix[row2][(col2 - 1) % 5])
#             elif col1 == col2:  # В одном столбце
#                 decrypted_text.append(self.matrix[(row1 - 1) % 5][col1])
#                 decrypted_text.append(self.matrix[(row2 - 1) % 5][col2])
#             else:  # Прямоугольник
#                 decrypted_text.append(self.matrix[row1][col2])
#                 decrypted_text.append(self.matrix[row2][col1])

#         return "".join(decrypted_text)
class PlayfairCipher:
    # Инициализация класса PlayfairCipher
    def __init__(self, n=256, key="example"):
        self.n = n  # Размер таблицы (по умолчанию 256x256 символов)
        self.key = key  # Ключ для формирования таблицы
        self.table = self.create_matrix_unicode()  # Создание таблицы символов
        self.placehold_symbol = chr(161)  # Символ-заполнитель для биграмм с повторяющимися символами ('¡')

    # Создание таблицы символов Unicode на основе ключа
    def create_matrix_unicode(self):
        # Инициализация пустой таблицы размером n x n
        table_unicode = [[None for _ in range(self.n)] for _ in range(self.n)]
        used_chars = set()  # Множество для хранения уже добавленных символов
        x, y = 0, 0  # Координаты текущей позиции в таблице

        # Добавление символов ключа в таблицу
        for char in self.key:
            if char not in used_chars:  # Добавляем только уникальные символы
                table_unicode[x][y] = char
                y += 1
                if y >= self.n:  # Переход на новую строку, если конец строки
                    y = 0
                    x += 1
                used_chars.add(char)  # Помечаем символ как использованный

        # Добавление оставшихся символов Unicode в таблицу
        for i in range(self.n * self.n):
            char = chr(i)  # Символ Unicode
            if char not in used_chars:  # Добавляем только неиспользованные символы
                table_unicode[x][y] = char
                y += 1
                if y >= self.n:  # Переход на новую строку
                    y = 0
                    x += 1

        return table_unicode  # Возвращаем заполненную таблицу

    # Поиск позиции символа в таблице
    def _find_position(self, char):
        for i in range(self.n):  # Перебираем строки
            for j in range(self.n):  # Перебираем столбцы
                if self.table[i][j] == char:  # Если символ найден
                    return i, j  # Возвращаем координаты
        return None, None  # Если символ не найден, возвращаем None

    # Разбиение текста на биграммы (пары символов)
    def _bigrams(self, text):
        bigrams = []  # Список для хранения биграмм
        i = 0

        # Генерация биграмм
        while i < len(text) - 1:
            if text[i] != text[i + 1]:  # Если символы в паре разные
                bigrams.append(text[i:i + 2])  # Добавляем пару
                i += 2  # Переходим к следующей паре
            else:  # Если символы одинаковы
                bigrams.append(text[i] + self.placehold_symbol)  # Добавляем символ и заполнитель
                i += 1

        if i < len(text):  # Если длина текста нечетная
            bigrams.append(text[i] + self.placehold_symbol)  # Добавляем последний символ с заполнителем

        return bigrams  # Возвращаем список биграмм

    # Шифрование текста
    def encrypt(self, source_text):
        cipher_text = ""  # Результирующий зашифрованный текст
        bigrams = self._bigrams(source_text)  # Разбиваем текст на биграммы

        for bi in bigrams:  # Обрабатываем каждую биграмму
            row1, col1 = self._find_position(bi[0])  # Находим позицию первого символа
            row2, col2 = self._find_position(bi[1])  # Находим позицию второго символа

            if row1 == row2:  # Если символы в одной строке
                col1 = (col1 + 1) % self.n  # Сдвигаем первый символ вправо
                col2 = (col2 + 1) % self.n  # Сдвигаем второй символ вправо
            elif col1 == col2:  # Если символы в одном столбце
                row1 = (row1 + 1) % self.n  # Сдвигаем первый символ вниз
                row2 = (row2 + 1) % self.n  # Сдвигаем второй символ вниз
            else:  # Если символы образуют прямоугольник
                col1, col2 = col2, col1  # Меняем столбцы местами

            cipher_text += self.table[row1][col1] + self.table[row2][col2]  # Добавляем зашифрованные символы

        return cipher_text  # Возвращаем зашифрованный текст

    # Расшифровка текста
    def decrypt(self, source_text):
        plain_text = ""  # Результирующий расшифрованный текст
        bigrams = [source_text[i:i + 2] for i in range(0, len(source_text), 2)]  # Разбиваем текст на биграммы

        for bi in bigrams:  # Обрабатываем каждую биграмму
            row1, col1 = self._find_position(bi[0])  # Находим позицию первого символа
            row2, col2 = self._find_position(bi[1])  # Находим позицию второго символа

            if row1 == row2:  # Если символы в одной строке
                col1 = (col1 - 1) % self.n  # Сдвигаем первый символ влево
                col2 = (col2 - 1) % self.n  # Сдвигаем второй символ влево
            elif col1 == col2:  # Если символы в одном столбце
                row1 = (row1 - 1) % self.n  # Сдвигаем первый символ вверх
                row2 = (row2 - 1) % self.n  # Сдвигаем второй символ вверх
            else:  # Если символы образуют прямоугольник
                col1, col2 = col2, col1  # Меняем столбцы местами

            plain_text += self.table[row1][col1] + self.table[row2][col2]  # Добавляем расшифрованные символы

        return plain_text.replace(self.placehold_symbol, "")  # Убираем символ-заполнитель и возвращаем текст


# Пример использования
# cipher = PlayfairCipher(key="KEYWORD")  # Создаем объект PlayfairCipher с ключом "KEYWORD"
# text = "HELLO"  # Текст для шифрования
# enc = cipher.encrypt(text)  # Шифруем текст
# print("Encrypted:", enc)  # Выводим зашифрованный текст
# dec = cipher.decrypt(enc)  # Расшифровываем текст
# print("Decrypted:", dec)  # Выводим расшифрованный текст

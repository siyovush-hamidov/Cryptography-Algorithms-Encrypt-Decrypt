class PlayfairCipher:
    def create_matrix(key):
        matrix = []
        used_chars = set()
        char_table = "".join(chr(i).encode('latin1').decode('cp1251', errors='replace') for i in range(32, 256))
        
        # Убираем дубликаты в ключе
        key_chars = [char for char in key if char not in used_chars and not used_chars.add(char)]
        
        # Заполняем таблицу ключевыми символами
        current_index = 0
        for char in key_chars:
            matrix.append(char)
            current_index += 1

        # Заполняем таблицу оставшимися символами
        for char in char_table:
            if char not in used_chars:
                matrix.append(char)

        return matrix

    def get_symbol_position(symbol, matrix):
        index = matrix.index(symbol)
        return {'row': index // 16, 'col': index % 16}
    
    @staticmethod
    def encrypt_ascii(text, key):
        matrix = PlayfairCipher.create_matrix(key)
        encrypted_text = ''
        text_pairs = []
        separator=' '

        i = 0
        while i < len(text):
            char1 = text[i]
            char2 = text[i + 1] if i + 1 < len(text) else separator

            if char1 == char2:
                pair = char1 + separator
                i += 1  # Пропускаем только первый символ пары
            else:
                pair = char1 + char2
                i += 2  # Переходим к следующей паре

            text_pairs.append(pair)

        # # Разбиваем текст на пары символов
        # for i in range(0, len(text), 2):
        #     pair = text[i]
        #     if i + 1 < len(text):
        #         pair += text[i + 1]
        #     else:
        #         pair += ' '  # Добавляем пробел в конце, если нечётное количество символов
        #     text_pairs.append(pair)

        # Шифруем каждую пару
        for pair in text_pairs:
            pos1 = PlayfairCipher.get_symbol_position(pair[0], matrix)
            pos2 = PlayfairCipher.get_symbol_position(pair[1], matrix)

            if pos1['row'] == pos2['row']:  # Если символы в одной строке
                pos1['col'] = (pos1['col'] + 1) % 16
                pos2['col'] = (pos2['col'] + 1) % 16
            elif pos1['col'] == pos2['col']:  # Если символы в одном столбце
                pos1['row'] = (pos1['row'] + 1) % 14
                pos2['row'] = (pos2['row'] + 1) % 14
            else:  # Если символы в разных строках и столбцах
                pos1['col'], pos2['col'] = pos2['col'], pos1['col']

            encrypted_text += matrix[pos1['row'] * 16 + pos1['col']] + matrix[pos2['row'] * 16 + pos2['col']]

        return encrypted_text

    @staticmethod
    def preprocess_text(text):
        # Если длина текста нечётная, добавляем символ 'X'
        if len(text) % 2 != 0:
            text += 'x'
        
        return text

    # Дешифрование текста
    @staticmethod
    def decrypt_ascii(text, key):
        text = PlayfairCipher.preprocess_text(text)
        matrix = PlayfairCipher.create_matrix(key)
        decrypted_text = ''
        text_pairs = []

        # Разбиваем текст на пары символов
        for i in range(0, len(text), 2):
            pair = text[i] + text[i + 1]
            text_pairs.append(pair)

        # Дешифруем каждую пару
        for pair in text_pairs:
            if pair[0] == pair[1]:
                decrypted_text += pair
                continue
            
            pos1 = PlayfairCipher.get_symbol_position(pair[0], matrix)
            pos2 = PlayfairCipher.get_symbol_position(pair[1], matrix)
            
            if pos1['row'] == pos2['row']:  # Если символы в одной строке
                pos1['col'] = (pos1['col'] - 1 + 16) % 16
                pos2['col'] = (pos2['col'] - 1 + 16) % 16
            elif pos1['col'] == pos2['col']:  # Если символы в одном столбце
                pos1['row'] = (pos1['row'] - 1 + 14) % 14
                pos2['row'] = (pos2['row'] - 1 + 14) % 14
            else:  # Если символы в разных строках и столбцах
                pos1['col'], pos2['col'] = pos2['col'], pos1['col']
            
            decrypted_text += matrix[pos1['row'] * 16 + pos1['col']] + matrix[pos2['row'] * 16 + pos2['col']]

        return decrypted_text
class PlayfairCipher:
    def __init__(self, n=256, key="example"):
        self.n = n
        self.key = key
        self.table = self.create_matrix_unicode()
        self.placehold_symbol = chr(161)  # '¡'

    def create_matrix_unicode(self):
        table_unicode = [[None for _ in range(self.n)] for _ in range(self.n)]
        used_chars = set()
        x, y = 0, 0

        for char in self.key:
            if char not in used_chars:
                table_unicode[x][y] = char
                y += 1
                if y >= self.n:
                    y = 0
                    x += 1
                used_chars.add(char)

        for i in range(self.n * self.n):
            char = chr(i)
            if char not in used_chars:
                table_unicode[x][y] = char
                y += 1
                if y >= self.n:
                    y = 0
                    x += 1

        return table_unicode

    def _find_position(self, char):
        for i in range(self.n):
            for j in range(self.n):
                if self.table[i][j] == char:
                    return i, j
        return None, None

    def _bigrams(self, text):
        bigrams = []
        i = 0

        while i < len(text) - 1:
            if text[i] != text[i + 1]:
                bigrams.append(text[i:i + 2])
                i += 2
            else:
                bigrams.append(text[i] + self.placehold_symbol)
                i += 1

        if i < len(text):
            bigrams.append(text[i] + self.placehold_symbol)

        return bigrams

    def encrypt(self, source_text):
        cipher_text = ""
        bigrams = self._bigrams(source_text)

        for bi in bigrams:
            row1, col1 = self._find_position(bi[0])
            row2, col2 = self._find_position(bi[1])

            if row1 == row2:
                col1 = (col1 + 1) % self.n
                col2 = (col2 + 1) % self.n
            elif col1 == col2:
                row1 = (row1 + 1) % self.n
                row2 = (row2 + 1) % self.n
            else:
                col1, col2 = col2, col1

            cipher_text += self.table[row1][col1] + self.table[row2][col2]

        return cipher_text

    def decrypt(self, source_text):
        plain_text = ""
        bigrams = [source_text[i:i + 2] for i in range(0, len(source_text), 2)]

        for bi in bigrams:
            row1, col1 = self._find_position(bi[0])
            row2, col2 = self._find_position(bi[1])

            if row1 == row2:
                col1 = (col1 - 1) % self.n
                col2 = (col2 - 1) % self.n
            elif col1 == col2:
                row1 = (row1 - 1) % self.n
                row2 = (row2 - 1) % self.n
            else:
                col1, col2 = col2, col1

            plain_text += self.table[row1][col1] + self.table[row2][col2]

        return plain_text.replace(self.placehold_symbol, "")


# Example usage
cipher = PlayfairCipher(key="KEYWORD")
text = "HELLO"
enc = cipher.encrypt(text)
print("Encrypted:", enc)
dec = cipher.decrypt(enc)
print("Decrypted:", dec)

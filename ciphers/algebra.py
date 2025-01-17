class AlgebraOfMatrix:
    ASCII_START = 9
    ASCII_END = 65535
    MOD = 227
    ENCODING = 'windows-1251'

    def __init__(self, key):
        self.matrixSize = 3
        self.keyMatrix = self.createKeyMatrix(key)
        self.inverseKeyMatrix = self.computeInverseKeyMatrix(self.keyMatrix)

    def createKeyMatrix(self, key):
        key = self.prepareKey(key)
        matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        keyBytes = key.encode(self.ENCODING)
        index = 0

        for i in range(3):
            for j in range(3):
                matrix[i][j] = self.byteToIndex(keyBytes[index])
                index += 1

        # print("Матрица ключа:")
        # self.printMatrix(matrix)
        return matrix

    def prepareKey(self, key):
        if len(key) > 9:
            return key[0:9]
        elif len(key) < 9:
            return "{:<9}".format(key)
        return key

    def encrypt(self, message):
        message = self.prepareMessage(message)
        messageBytes = message.encode(self.ENCODING)
        cipherchars = [' '] * len(message)

        for i in range(0, len(message), 3):
            messageVector = [0, 0, 0]
            for j in range(3):
                messageVector[j] = self.byteToIndex(messageBytes[i+j])

            # print("\nВектор сообщения:")
            # self.printVector(messageVector)

            resultVector = self.multiplyMatrixAndVector(self.keyMatrix, messageVector)

            # print("Результирующий вектор:")
            # self.printVector(resultVector)

            for j in range(3):
                cipherchars[i + j] = self.indexTochar(resultVector[j])

        result = ""
        for cipherchar in cipherchars:
            result += cipherchar
        return result

    def decrypt(self, text):
        plainchars = bytearray(len(text))
        deter = self.determinant(self.keyMatrix)

        for i in range(0, len(text), 3):
            cipherVector = [0, 0, 0]
            for j in range(3):
                cipherVector[j] = self.charToIndex(text[i+j])

            resultVector = self.multiplyMatrixAndVector(self.inverseKeyMatrix, cipherVector)
            # print("Result vector: ")
            # self.printVector(resultVector)

            for j in range(3):
                value = self.indexToByte(resultVector[j]//deter)
                plainchars[i + j] = value % 256  # Ensure the value is in valid byte range

        return plainchars.decode(self.ENCODING)

    def multiplyMatrixAndVector(self, matrix, vector):
        result = [0, 0, 0]
        for i in range(3):
            result[i] = 0
            for j in range(3):
                result[i] += matrix[i][j] * vector[j]
        return result

    def computeInverseKeyMatrix(self, matrix):
        adjugate = self.adjugateMatrix(matrix)
        # print("reverse matrix: ")
        # self.printMatrix(adjugate)
        return adjugate

    def determinant(self, matrix):
        det = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) - \
              matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) + \
              matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
        # print("Determinant= " + str(det))
        return det

    def adjugateMatrix(self, matrix):
        adj = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        adj[0][0] = matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]
        adj[0][1] = -(matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        adj[0][2] = matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]
        adj[1][0] = -(matrix[0][1] * matrix[2][2] - matrix[0][2] * matrix[2][1])
        adj[1][1] = matrix[0][0] * matrix[2][2] - matrix[0][2] * matrix[2][0]
        adj[1][2] = -(matrix[0][0] * matrix[2][1] - matrix[0][1] * matrix[2][0])
        adj[2][0] = matrix[0][1] * matrix[1][2] - matrix[0][2] * matrix[1][1]
        adj[2][1] = -(matrix[0][0] * matrix[1][2] - matrix[0][2] * matrix[1][0])
        adj[2][2] = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        adj = self.transponseMatrix(adj)
        return adj

    def transponseMatrix(self, mm):
        tr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        tr[0][0] = mm[0][0]
        tr[1][1] = mm[1][1]
        tr[2][2] = mm[2][2]
        tr[0][1] = mm[1][0]
        tr[0][2] = mm[2][0]
        tr[1][0] = mm[0][1]
        tr[1][2] = mm[2][1]
        tr[2][0] = mm[0][2]
        tr[2][1] = mm[1][2]
        return tr

    def modInverse(self, a, m):
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 1

    def prepareMessage(self, message):
        while len(message) % 3 != 0:
            message += " "
        return message

    def byteToIndex(self, b):
        value = int.from_bytes([b], byteorder='big', signed=False) if isinstance(b, int) else b
        # print(str(value) + "\t")
        # print()
        if value < self.ASCII_START or value > self.ASCII_END:
            raise ValueError("Неподдерживаемый символ: " + chr(value))
        elif value == 9:
            return 1
        elif value == 10:
            return 2
        elif value == 13:
            return 3
        else:
            return value - 28

    def indexToByte(self, index):
        if index == 1:
            return 9
        elif index == 2:
            return 10
        elif index == 3:
            return 13
        else:
            value = index + 28
            return value % 256  # Ensure the value is in valid byte range

    def printMatrix(self, matrix):
        for i in range(3):
            for j in range(3):
                print(str(matrix[i][j]) + "\t", end="")
            print()

    def printVector(self, vector):
        for value in vector:
            print(str(value) + "\t", end="")
        print()

    def charToIndex(self, a):
        return ord(a)

    def indexTochar(self, a):
        return chr(a)
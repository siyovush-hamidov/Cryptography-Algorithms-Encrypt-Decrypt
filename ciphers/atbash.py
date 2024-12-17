import re

class AtbashCipher:
    @staticmethod
    def reverse_message(message: str) -> str:
        return message[::-1]

    @staticmethod
    def reverse_sentence(message: str) -> str:
        # Split the message into sentences using regex
        sentences = re.split(r'([.!?])', message)
        reversed_sentences = []
        
        for i in range(0, len(sentences) - 1, 2):
            sentence = sentences[i]
            punctuation = sentences[i + 1]
            # Reverse the sentence and append the punctuation
            reversed_sentences.append(punctuation + AtbashCipher.reverse_message(sentence))
        return ''.join(reversed_sentences)

    @staticmethod
    def reverse_word(message: str) -> str:
        tokens = re.findall(r'\w+|[^\w\s]|[\s]+', message)
        reversed_tokens = []
        
        for token in tokens:
            if token.isalpha():
                reversed_tokens.append(token[::-1])
            elif token.isspace():
                reversed_tokens.append(token)
            else:
                reversed_tokens.append(token)
        return ''.join(reversed_tokens)
    
print(AtbashCipher.reverse_message("Привет! Пока."))
print(AtbashCipher.reverse_sentence("Привет, как дела? Пока."))
print(AtbashCipher.reverse_word("Привет! Пока."))
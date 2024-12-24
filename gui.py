import customtkinter as ctk
from ciphers import *
import itertools

class CryptographyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cryptography Algorithms")
        self.geometry(f"{self.winfo_screenwidth()}x{
                      self.winfo_screenheight()}")
        # self.resizable(False, False)
        self.available_ciphers = ["Caesar", "Playfair", "RSA", "Vertical", "Vijiner"]

        # Frame for cipher and encoding options
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(pady=10, fill=ctk.X)

        # Radio buttons for ASCII and UNICODE
        self.radio_var = ctk.StringVar()
        self.radio_var.set("ASCII")

        ascii_radio = ctk.CTkRadioButton(
            options_frame, text="ASCII", variable=self.radio_var, value="ASCII")
        ascii_radio.pack(side=ctk.LEFT, padx=5)

        unicode_radio = ctk.CTkRadioButton(
            options_frame, text="UNICODE", variable=self.radio_var, value="UNICODE")
        unicode_radio.pack(side=ctk.LEFT, padx=5)
        # для ввода ключевого слова
        self.keyword_entry = ctk.CTkEntry(
            options_frame, placeholder_text="Keyword (if applicable)", width=150)
        self.keyword_entry.pack(side=ctk.LEFT, padx=5)
        self.keyword_entry.insert(-1, "")
        # | ДЛЯ ХАРДКОДА | НЕ СТИРАТЬ!

        # Input Memo
        self.input_text = ctk.CTkTextbox(
            self, width=700, height=self.winfo_screenheight() // 4)
        self.input_text.pack(pady=5, fill=ctk.X)

        self.input_text.insert("1.0", """""") 
        # ЭТО НУЖНО ЧТОБЫ СДЕЛАТЬ ХАРДКОД / ДЛЯ ПРОВЕРКИ / НЕ СТИРАТЬ!!!

        # Frame for buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10, fill=ctk.X)

        encrypt_button = ctk.CTkButton(
            button_frame, text="Encrypt", command=self.encrypt, width=self.winfo_screenwidth() // 2)
        encrypt_button.pack(side=ctk.LEFT, expand=True, padx=10)

        decrypt_button = ctk.CTkButton(
            button_frame, text="Decrypt", command=self.decrypt, width=self.winfo_screenwidth() // 2)
        decrypt_button.pack(side=ctk.LEFT, expand=True, padx=10)

        # Output Memo
        self.output_text = ctk.CTkTextbox(
            self, width=700, height=self.winfo_screenheight() // 2)
        self.output_text.pack(pady=5, fill=ctk.X)

    def encrypt(self):
        # Получаем параметры из UI
        input_text = self.input_text.get("1.0", ctk.END).strip()
        keyword = self.keyword_entry.get().strip()
        mode = self.radio_var.get()

        # Переменная для хранения результатов
        results = []

        # Проверка на пустое значение keyword
        if not keyword.strip():
            self.output_text.delete("1.0", ctk.END)
            self.output_text.insert(ctk.END, "Error: Keyword cannot be empty.")
            return

        # Проверка режима
        if mode not in ["ASCII", "UNICODE"]:
            self.output_text.delete("1.0", ctk.END)
            self.output_text.insert(ctk.END, "Error: Invalid mode selected.")
            return

        try:
            # Генерация ключей
            words = keyword.split()

            for cipher in self.available_ciphers:
                if cipher == "Caesar":
                    # Генерируем числовые ключи для Caesar
                        
                    key_combinations = []
                    if(keyword.isdigit()):
                        key_combinations.append(int(keyword))
                    for word in words:
                        key_combinations.append(len(word))
                    key_combinations = sorted(set(key_combinations))
                else:
                    # Генерируем текстовые ключи для остальных шифров
                    key_combinations = []
                    max_words_in_combination = 3  # Ограничение
                    for i in range(1, min(len(words), max_words_in_combination) + 1):
                        for combination in itertools.permutations(words, i):
                            key_combinations.append(" ".join(combination))
                    key_combinations = sorted(set(key_combinations))

                # Перебор ключей
                for key in key_combinations:
                    try:
                        if mode == "ASCII":
                            if cipher == "Caesar":
                                result = CaesarCipher.encrypt_ascii(input_text, int(key))
                            elif cipher == "Playfair":
                                result = PlayfairCipher.encrypt_ascii(input_text, key)
                            elif cipher == "RSA":
                                result = RSACipher.encrypt_ascii(input_text, key)
                            elif cipher == "Vertical":
                                result = VerticalCipher.encrypt_ascii(input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.encrypt_ascii(input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.encrypt(input_text, key)    
                            else:
                                raise ValueError("Unsupported cipher!")
                        else:
                            if cipher == "Caesar":
                                result = CaesarCipher.encrypt_unicode(input_text, int(key))
                            elif cipher == "Playfair":
                                result = PlayfairCipher.encrypt_unicode(input_text, key)
                            elif cipher == "RSA":
                                result = RSACipher.encrypt_unicode(input_text, key)
                            elif cipher == "Vertical":
                                result = VerticalCipher.encrypt_unicode(input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.encrypt_unicode(input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.encrypt(input_text, key)    
                            else:
                                raise ValueError("Unsupported cipher!")
                        # Добавляем успешный результат
                        results.append(
                            f"CIPHER: {cipher.upper()} | KEYWORD: {key}\nRESULT:\n{result}\n{'=' * 70}"
                        )
                    except Exception as e:
                        # Добавляем информацию об ошибке
                        results.append(
                            f"CIPHER: {cipher.upper()} | KEYWORD: {key}\nERROR:\n{str(e)}\n{'=' * 70}"
                        )
        except Exception as e:
            results.append(f"Error: {str(e)}")

        # Вывод всех результатов в output_text
        self.output_text.delete("1.0", ctk.END)
        self.output_text.insert(ctk.END, "\n".join(results))

    def decrypt(self):
        # Получаем параметры из UI
        input_text = self.input_text.get("1.0", ctk.END).strip()
        keyword = self.keyword_entry.get().strip()
        mode = self.radio_var.get()
        
        # Переменная для хранения результатов
        results = []

        # Проверка на пустое значение keyword
        if not keyword.strip():
            self.output_text.delete("1.0", ctk.END)
            self.output_text.insert(ctk.END, "Error: Keyword cannot be empty.")
            return

        # Проверка режима
        if mode not in ["ASCII", "UNICODE"]:
            self.output_text.delete("1.0", ctk.END)
            self.output_text.insert(ctk.END, "Error: Invalid mode selected.")
            return

        try:
            # Генерация ключей
            words = keyword.split()

            for cipher in self.available_ciphers:
                if cipher == "Caesar":
                    # Генерируем числовые ключи для Caesar
                    key_combinations = []
                    for word in words:
                        key_combinations.append(len(word))
                    key_combinations = sorted(set(key_combinations))
                else:
                    # Генерируем текстовые ключи для остальных шифров
                    key_combinations = []
                    max_words_in_combination = 3  # Ограничение
                    for i in range(1, min(len(words), max_words_in_combination) + 1):
                        for combination in itertools.permutations(words, i):
                            key_combinations.append(" ".join(combination))
                    key_combinations = sorted(set(key_combinations))

                # Перебор ключей
                for key in key_combinations:
                    try:
                        if mode == "ASCII":
                            if cipher == "Caesar":
                                result = CaesarCipher.decrypt_ascii(input_text, int(key))
                            elif cipher == "Playfair":
                                result = PlayfairCipher.decrypt_ascii(input_text, key)
                            elif cipher == "RSA":
                                result = RSACipher.decrypt_ascii(input_text, key)
                            elif cipher == "Vertical":
                                result = VerticalCipher.decrypt_ascii(input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.decrypt_ascii(input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.decrypt(input_text, key)    
                            else:
                                raise ValueError("Unsupported cipher!")
                        else:
                            if cipher == "Caesar":
                                result = CaesarCipher.decrypt_unicode(input_text, int(key))
                            elif cipher == "Playfair":
                                result = PlayfairCipher.decrypt_unicode(input_text, key)
                            elif cipher == "RSA":
                                result = RSACipher.decrypt_unicode(input_text, key)
                            elif cipher == "Vertical":
                                result = VerticalCipher.decrypt_unicode(input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.decrypt_unicode(input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.decrypt(input_text, key)    
                            else:
                                raise ValueError("Unsupported cipher!")
                        # Добавляем успешный результат
                        results.append(
                            f"CIPHER: {cipher.upper()} | DECRYPT | KEYWORD: {key}\nRESULT:\n{result}\n{'=' * 70}"
                        )
                    except Exception as e:
                        # Добавляем информацию об ошибке
                        results.append(
                            f"CIPHER: {cipher.upper()} | DECRYPT | KEYWORD: {key}\nERROR:\n{str(e)}\n{'=' * 70}"
                        )
        except Exception as e:
            results.append(f"Error: {str(e)}")

        # Вывод всех результатов в output_text
        self.output_text.delete("1.0", ctk.END)
        self.output_text.insert(ctk.END, "\n".join(results))
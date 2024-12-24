import customtkinter as ctk
from ciphers import *
import itertools


class CryptographyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Для плейфера нужен объект класса поэтому ОБЪЯВЛЕНИЯ ОБЪЕКТОВ ЗДЕСЬ
        self.playfairCipherObj = PlayfairCipher("")
        self.title("Cryptography Algorithms")
        self.geometry(f"{self.winfo_screenwidth()}x{
                      self.winfo_screenheight()}")
        # self.resizable(False, False)

        # Frame for cipher and encoding options
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(pady=10, fill=ctk.X)

        # self.cipher_combobox = ctk.CTkComboBox(options_frame, values=[
        #     "Atbash", "Caesar", "Playfair", "RSA", "Vertical", "Vijiner"])
        # self.cipher_combobox.pack(side=ctk.LEFT, padx=5)
        # self.cipher_combobox.set("Atbash")

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
        self.keyword_entry.insert(-1, "Хамидов Сиёвуш Халифабобоевич")

        # Input Memo
        self.input_text = ctk.CTkTextbox(
            self, width=700, height=self.winfo_screenheight() // 4)
        self.input_text.pack(pady=5, fill=ctk.X)
        self.input_text.insert("1.0", "¤РФиТЯХОЕЭЪЖЩЗВИФиОЬОБЕЬЯЙЯМГЙмМЙнФєЛиХТЯФЅаОЦЛЫКїАСЪдЦПЙОЬФДдКФммРЛРЗЖТЩЦХаЮХКЪЪТЮРѕаРШЧСКБаЯЯДЯФВИЦИРоТРНЦИдЪР»ЕЮиХбЫєСЮКЙЫПГаЭХМХКЗЬмМТгР№НЪЩЦквТТЪСдТЗФТСУаЫРЖТФцд°в№ЕлЪЙЩЮВОЭЪМоЕГСЯМДЮУЗВМиУЬТГЖРИЙаУФаФХШЬТБАвРгъвЕАЭТФйФЅЕмТТаРЕОХиРЬИєТмЩСЦЙЅТиибвЦєКЮРЖЫРЖТииУЮР·ОРРРЬЛХПЪУМаКїИъиіЬЖГБЩИгоКВФЪШРОШЅЯмПДШТРВМНЦЯббаФиЧЯФµНМКПЦДµЕШгНоТєЖФФдУЗХИЭЧТЩЮјООИСЦбХПЬРЛРВВаЫШЙТХДРСММаЮХВЪПРЬИВОЭЪаоПєСМХОдКГНФШТРВВНЪЛТоРјНМТТЪНєНФздЯвВЕХцд°вТТЪФдЯНИЧМНдЬГПЕЦЪТЪв¶ЕУЦУОУВОЭЪМоДРСЮЫУОЗЗаЬНКЦОХДЪЩЦбСµаЦиМЫЦГРШИЪЦКбаМиМЫЦГРШИЪЦРВНМздПЗјОЫИХЫРЖТииЛОМАЮгИЙаУФаОиСУДГЗШЦКЫРЖТФиСОТИШСХМнвТТЪЛТоТєЖФФДьв¤РФФЙЮРБаШЦЗбФХСЧЫКЦФСаФХШЬТБАвРТЫПГнЮНПУМГМШЫСЦМµЦФЦСЫЭєаЭРХаЗБЫмРдЯТєДЭЪЖОвЖВлПМъвДРСМСОЙВАгНСЫЭєаРУгоР¶РМЙТаМЅаФиУУТєДМЯМоУ·ЕРНСЦЛбаЭЦХаВ·ЛлжЭЦЧХГЪЩЧТВЕСЮКЙЫПИЮмЪДЧПИо")

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

    # def encrypt(self):
    #     cipher = self.cipher_combobox.get()
    #     mode = self.radio_var.get()
    #     input_text = self.input_text.get("1.0", ctk.END).strip()
    #     keyword = self.keyword_entry.get().strip()
    #     try:
    #         if mode == "ASCII":
    #             if cipher == "Atbash":
    #                 output_text = AtbashCipher.reverse_message(input_text)
    #             elif cipher == "Caesar":
    #                 # Проверка, является ли keyword числом
    #                 if keyword.isdigit() or (keyword.startswith('-') and keyword[1:].isdigit()):
    #                     intKey = int(keyword)
    #                 else:
    #                     intKey = len(keyword)

    #                 # Проверка диапазона ключа для числового значения
    #                 if intKey < -255 or intKey > 255:
    #                     raise ValueError("Key must be between -255 and 255!")
    #                 else:
    #                     output_text = CaesarCipher.encrypt_ascii(
    #                         input_text, intKey)
    #             elif cipher == "Playfair":
    #                 output_text = self.playfairCipherObj.encrypt_ascii(
    #                     input_text, keyword)
    #             elif cipher == "RSA":
    #                 output_text = RSACipher.encrypt_ascii(input_text, keyword)
    #             elif cipher == "Vertical":
    #                 output_text = VerticalCipher.encrypt_ascii(input_text)
    #             elif cipher == "Vijiner":
    #                 output_text = VigenereCipher.encrypt_ascii(
    #                     input_text, keyword)
    #             else:
    #                 raise ValueError("Unsupported cipher!")
    #         else:
    #             if cipher == "Atbash":
    #                 output_text = AtbashCipher.reverse_message(input_text)
    #             elif cipher == "Caesar":
    #                 output_text = CaesarCipher.encrypt_unicode(
    #                     input_text, int(keyword))
    #             elif cipher == "Playfair":
    #                 output_text = PlayfairCipher.encrypt_unicode(
    #                     input_text, keyword)
    #             elif cipher == "RSA":
    #                 output_text = RSACipher.encrypt_unicode(
    #                     input_text, keyword)
    #             elif cipher == "Vertical":
    #                 output_text = VerticalCipher.encrypt_unicode(input_text)
    #             else:
    #                 raise ValueError("Unsupported cipher!")
    #     except Exception as e:
    #         output_text = f"Error: {str(e)}"
    #     self.output_text.delete("1.0", ctk.END)
    #     self.output_text.insert(ctk.END, output_text)

    import itertools


    def encrypt(self):
        # Получаем параметры из UI
        input_text = self.input_text.get("1.0", ctk.END).strip()
        keyword = self.keyword_entry.get().strip()
        mode = self.radio_var.get()

        # Список доступных шифров
        available_ciphers = ["Caesar", "Playfair", "RSA", "Vertical", "Vijiner","DESS","Gronsfeld"]

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

            for cipher in available_ciphers:
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
                                result = CaesarCipher.encrypt_ascii(input_text, int(key))
                            elif cipher == "Playfair":
                                result = self.playfairCipherObj.encrypt_ascii(input_text, key)
                            elif cipher == "RSA":
                                result = RSACipher.encrypt_ascii(input_text, key)
                            elif cipher == "Vertical":
                                result = VerticalCipher.encrypt_ascii(input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.encrypt_ascii(input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.encrypt_ascii(input_text, key)
                            elif cipher == "Gronsfeld":
                                result = GronsfeldCipher.encrypt_ascii(input_text, key)        
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
                                result = CustomDESCipher.encrypt_unicode(input_text, key)
                            elif cipher == "Gronsfeld":
                                result = GronsfeldCipher.encrypt_unicode(input_text, key)        
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

        # Список доступных шифров
        available_ciphers = ["Caesar", "Playfair", "RSA", "Vertical", "Vijiner", "DESS","Gronsfeld"]

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

            for cipher in available_ciphers:
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
                                result = self.playfairCipherObj.decrypt_ascii(input_text, key)
                            elif cipher == "RSA":
                                result = RSACipher.decrypt_ascii(input_text, key)
                            elif cipher == "Vertical":
                                result = VerticalCipher.decrypt_ascii(input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.decrypt_ascii(input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.decrypt_ascii(input_text, key)
                            elif cipher == "Gronsfeld":
                                result = GronsfeldCipher.decrypt_ascii(input_text, key)        
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
                                result = CustomDESCipher.decrypt_unicode(input_text, key)
                            elif cipher == "Gronsfeld":
                                result = GronsfeldCipher.decrypt_unicode(input_text, key)        
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

    # def decrypt(self):
    #     cipher = self.cipher_combobox.get()
    #     mode = self.radio_var.get()
    #     input_text = self.input_text.get("1.0", ctk.END).strip()
    #     keyword = self.keyword_entry.get().strip()
    #     try:
    #         if mode == "ASCII":
    #             if cipher == "Atbash":
    #                 output_text = AtbashCipher.reverse_message(input_text)
    #             elif cipher == "Caesar":
    #                 output_text = CaesarCipher.decrypt_ascii(
    #                     input_text, int(keyword))
    #             elif cipher == "Playfair":
    #                 output_text = PlayfairCipher.decrypt_ascii(
    #                     input_text, keyword)
    #             elif cipher == "RSA":
    #                 output_text = RSACipher.decrypt_ascii(input_text, keyword)
    #             elif cipher == "Vertical":
    #                 output_text = VerticalCipher.decrypt_ascii(input_text)
    #             elif cipher == "Vijiner":
    #                 output_text = VigenereCipher.decrypt_ascii(
    #                     input_text, keyword)
    #             else:
    #                 raise ValueError("Unsupported cipher!")
    #         else:
    #             if cipher == "Atbash":
    #                 output_text = AtbashCipher.reverse_message(input_text)
    #             elif cipher == "Caesar":
    #                 output_text = CaesarCipher.decrypt_unicode(
    #                     input_text, int(keyword))
    #             elif cipher == "Playfair":
    #                 output_text = PlayfairCipher.decrypt_unicode(
    #                     input_text, keyword)
    #             elif cipher == "RSA":
    #                 output_text = RSACipher.decrypt_unicode(
    #                     input_text, keyword)
    #             elif cipher == "Vertical":
    #                 output_text = VerticalCipher.decrypt_unicode(input_text)
    #             else:
    #                 raise ValueError("Unsupported cipher!")
    #     except Exception as e:
    #         output_text = f"Error: {str(e)}"
    #     self.output_text.delete("1.0", ctk.END)
    #     self.output_text.insert(ctk.END, output_text)


# if __name__ == "__main__":
#     ctk.set_appearance_mode("dark")
#     ctk.set_default_color_theme("dark-blue")
#     app = CryptographyApp()
#     app.mainloop()

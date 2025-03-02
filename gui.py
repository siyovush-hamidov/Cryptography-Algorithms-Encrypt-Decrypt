import customtkinter as ctk
from ciphers import *
import itertools
from sympy import isprime

class CryptographyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cryptography Algorithms")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")

        self.available_ciphers = ["All", "Caesar", "Playfair", "RSA", "Vertical", "Vijiner", "DESS", "Gronsfeld", "Hill", "Algebra"]

        options_frame = ctk.CTkFrame(self)
        options_frame.pack(pady=10, fill=ctk.X)
        
        self.radio_var = ctk.StringVar()
        self.radio_var.set("ASCII")

        ascii_radio = ctk.CTkRadioButton(
            options_frame, text="ASCII", variable=self.radio_var, value="ASCII")
        ascii_radio.pack(side=ctk.LEFT, padx=5)

        unicode_radio = ctk.CTkRadioButton(
            options_frame, text="UNICODE", variable=self.radio_var, value="UNICODE")
        unicode_radio.pack(side=ctk.LEFT, padx=5)

        # Key Generation Mode: Single Words/Combination of Words
        self.key_mode_var = ctk.StringVar()
        self.key_mode_var.set("Single Words")  # Default to Single Words

        single_words_radio = ctk.CTkRadioButton(
            options_frame, text="Single Words", variable=self.key_mode_var, value="Single Words"
        )
        single_words_radio.pack(side=ctk.LEFT, padx=5)

        combo_words_radio = ctk.CTkRadioButton(
            options_frame, text="Combination of Words", variable=self.key_mode_var, value="Combination of Words"
        )
        combo_words_radio.pack(side=ctk.LEFT, padx=5)

        # для ввода ключевого слова
        # ComboBox for selecting cipher
        self.cipher_combobox = ctk.CTkComboBox(
            options_frame, values=self.available_ciphers, state="normal", width=150)
        self.cipher_combobox.set("All")  # Default option
        self.cipher_combobox.pack(side=ctk.LEFT, padx=5)

        # Keyword and RSA inputs
        self.keyword_entry = ctk.CTkEntry(
            options_frame, placeholder_text="Keyword (if applicable)", width=150)
        self.keyword_entry.pack(side=ctk.LEFT, padx=5)
        # self.keyword_entry.insert(-1, "КУПИ ПИВО!")
        # | ДЛЯ ХАРДКОДА | НЕ СТИРАТЬ!
        # ДЛЯ ВВОДА ПРОСТЫХ ЧИСЕЛ В RSA:
        self.rsa_p_edit = ctk.CTkEntry(
            options_frame, placeholder_text="RSA: p", width=60)
        self.rsa_p_edit.pack(side=ctk.LEFT, padx=5)
        # self.keyword_entry.insert(-1, "")
        self.rsa_q_edit = ctk.CTkEntry(
            options_frame, placeholder_text="RSA: q", width=60)
        self.rsa_q_edit.pack(side=ctk.LEFT, padx=5)
        self.rsa_d_edit = ctk.CTkEntry(
            options_frame, placeholder_text="RSA: d", width=60)
        self.rsa_d_edit.pack(side=ctk.LEFT, padx=5)
        self.input_text = ctk.CTkTextbox(
            self, width=700, height=self.winfo_screenheight() // 4)
        self.input_text.pack(pady=5, fill=ctk.X)
        # self.input_text.insert("1.0", """બڢгסज़ߊؚΊҊબӚҊؚۙвҊڶ٬۵Ӛؚàज़ίвס۵ௌ۵ؚબ५бڢҊؚڢбࠒҊڶۙвڢ˅ؚঌӚݷΊௌ੄َؚڤڢڤௌвؚͻҊબڢвҊͻҊڶۙвӚؚвؚбàΊàࠒҊҊؚҊؚڢڶвڢбڢݷΊӚҊؚۙҊгڢؚڢؚۙгڤàίӚَؚڤڢΞબௌߊؚڢΞסбڢƴؚסؚҊڤҊΞҊௌߊَؚڤڢбબҊ۵˅ؚঌڢгΊӚؚΒƴڢڢ۵סͻҊڶƴסҊؚвڢ੄ௌؚסίݪίӚؚסۙҊгڤӚϏססؚӚϏסڢӚબ٬ௌߊؚΒƴڢڢ۵סƴؚڶۙӚબסؚڶબסΞƴڢ۵ؚڢَӚڶௌ۵סؚסؚàбௌۙڢͻௌ۵סȈؚӚؚгબڢбӚબ٬ௌ੄ؚвڢҊௌ੄ؚƴڢশબסƴؚۙвڢڢбࠒҊؚڶَڢڶڢбҊَؚڤסвҊڶۙסؚƴؚסڶͻҊίڢвҊס५ؚݷסίסؚӚَؚબӚҊۙҊȈؚвڢ੄ӚَؚҊڤҊߊڢΊסؚۙвؚסà५َؚબڢڶƴڢڶۙ٬ؚݪؚסশڢڤ۵ӚϏסڢà५˅ؚǸশڢڤ۵ӚϏסڢӚज़ؚвڢ੄Ӛؚݪؚסশڢڤ۵ӚϏסڢڢҊَؚڤڢۙסвڢбڢڤڶۙвڢؚڶؚϏҊબ٬५ؚӚҊڶҊסज़ؚàࠒҊڤбӚؚвӚݷௌ۵ؚڶۙڤàƴۙàڤӚ۵َؚڤڢۙסвסƴӚȈَؚڢΊڤௌвӚؚҊгڢَؚڢબסۙסͻҊڶƴڢ੄ؚסؚڶڢϏסӚબ٬ڢ੄ؚڶסڶۙҊ۵ȈؚӚؚۙӚƴݷҊؚΊҊڶۙӚбסબסίӚϏססؚڢбࠒҊڶۙвӚؚסؚгڢڶàΊӚڤڶۙвӚَؚڤڢۙסвסƴӚ˅""")
        # # ЭТО НУЖНО ЧТОБЫ СДЕЛАТЬ ХАРДКОД / ДЛЯ ПРОВЕРКИ / НЕ СТИРАТЬ!!!

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
            self, width=700, height=self.winfo_screenheight() // 1.75)
        self.output_text.pack(pady=5, fill=ctk.X)

    def generate_keys(self, keyword):
        """
        Generate keys based on the selected key mode (Single Words or Combination of Words).
        """
        key_mode = self.key_mode_var.get()
        words = keyword.split()
        
        if key_mode == "Single Words":
            # Generate individual words as keys
            return sorted(set(words))
        elif key_mode == "Combination of Words":
            # Generate combinations of words as keys
            key_combinations = []
            max_words_in_combination = 3  # Limit for combinations
            for i in range(1, min(len(words), max_words_in_combination) + 1):
                for combination in itertools.permutations(words, i):
                    key_combinations.append(" ".join(combination))
            return sorted(set(key_combinations))
        else:
            raise ValueError("Invalid key mode selected.")

    # ВОТ ЭТА ФУНКЦИЯ НУЖНА ЧТОБЫ RSA МОГ ПЕРЕБИРАТЬ ВСЕВОЗМОЖНЫЕ ПАРЫ

    def generate_rsa_prime_pairs(self, p_min, p_max, q_min, q_max):
        """
        Генерация всех пар простых чисел (p, q) в заданных диапазонах.
        """
        primes_p = [p for p in range(p_min, p_max + 1) if isprime(p)]
        primes_q = [q for q in range(q_min, q_max + 1) if isprime(q)]
        return [(p, q) for p in primes_p for q in primes_q]

    def encrypt(self):
        # Получаем параметры из UI
        input_text = self.input_text.get("1.0", ctk.END).strip()
        keyword = self.keyword_entry.get().strip()
        mode = self.radio_var.get()
        
        rsa_p = self.rsa_p_edit.get().strip()
        rsa_q = self.rsa_q_edit.get().strip()
        rsa_d = self.rsa_d_edit.get().strip()
        
        if rsa_p and rsa_q and rsa_d and rsa_p.isdigit() and rsa_q.isdigit() and rsa_d.isdigit():
            rsa_p = int(rsa_p)
            rsa_q = int(rsa_q)
            rsa_d = int(rsa_d)
        selected_cipher = self.cipher_combobox.get()
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
            keys = []
            words = keyword.split()
            # Переменная для хранения результатов

            ciphers_to_use = [selected_cipher] if selected_cipher != "All" else self.available_ciphers[1:]

            for cipher in ciphers_to_use:
                if cipher == "Caesar":
                    # Генерируем числовые ключи для Caesar
                    if (keyword.isdigit()):
                        keys.append(int(keyword))
                    for word in words:
                        keys.append(len(word))
                else:
                    keys = self.generate_keys(keyword)

                # Перебор ключей
                for key in keys:
                    try:
                        if mode == "ASCII":
                            if cipher == "Caesar":
                                result = CaesarCipher.encrypt_ascii(
                                    input_text, int(key))
                            elif cipher == "Playfair":
                                result = PlayfairCipher.encrypt_ascii(
                                    input_text, key)
                            # elif cipher == "RSA":
                            #     p, q = int(self.rsa_p_edit.get()), int(self.rsa_q_edit.get())
                            #     result = RSACipher.encrypt_unicode(input_text, p, q)
                            elif cipher == "Vertical":
                                result = VerticalCipher.encrypt_ascii(
                                    input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.encrypt_ascii(
                                    input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.encrypt_ascii(
                                    input_text, key)
                            elif cipher == "Gronsfeld":
                                result = GronsfeldCipher.encrypt_ascii(
                                    input_text, key)
                            elif cipher == "Hill":
                                result = HillCipher.encrypt_ascii(
                                    input_text, key)                                
                            elif cipher == "Sha_1":
                                result = Sha_1.sha_1(key.encode('utf-8'))  
                            elif cipher == "Algebra":
                                 obj = AlgebraOfMatrix(key)
                                 result = obj.encrypt(
                                    input_text)                                     
                            else:
                                raise ValueError("Unsupported cipher!")
                        else:
                            if cipher == "Caesar":
                                result = CaesarCipher.encrypt_unicode(
                                    input_text, int(key))
                            elif cipher == "Playfair":
                                result = PlayfairCipher.encrypt_unicode(
                                    input_text, key)
                            elif cipher == "RSA":
                                result = RSACipher.encrypt(
                                    input_text, rsa_p, rsa_q, rsa_d)
                            elif cipher == "Vertical":
                                result = VerticalCipher.encrypt_unicode(
                                    input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.encrypt_unicode(
                                    input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.encrypt_unicode(
                                    input_text, key)
                            elif cipher == "Gronsfeld":
                                result = GronsfeldCipher.encrypt_unicode(
                                    input_text, key)
                            elif cipher == "Sha_1":
                                result = Sha_1.sha_1(key.encode('utf-8'))  
                            elif cipher == "Algebra":
                                obj = AlgebraOfMatrix(key)
                                result = obj.encrypt(
                                    input_text)    
                            else:
                                raise ValueError("Unsupported cipher!")
                        # Добавляем успешный результат
                        results.append(
                            f"CIPHER: {cipher.upper()} | KEYWORD: {key}\nRESULT:\n{
                                result}\n{'=' * 70}"
                        )
                    except Exception as e:
                        # Добавляем информацию об ошибке
                        results.append(
                            f"CIPHER: {cipher.upper()} | KEYWORD: {key}\nERROR:\n{
                                str(e)}\n{'=' * 70}"
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

        selected_cipher = self.cipher_combobox.get()
        
        rsa_p = self.rsa_p_edit.get().strip()
        rsa_q = self.rsa_q_edit.get().strip()
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
            prime_pairs_for_rsa = self.generate_rsa_prime_pairs(11, 99, 11, 300)
            words = keyword.split()
            keys = [] 
            ciphers_to_use = [selected_cipher] if selected_cipher != "All" else self.available_ciphers[1:]
            for cipher in ciphers_to_use:
                if cipher == "Caesar":
                    # Генерируем числовые ключи для Caesar
                    if (keyword.isdigit()):
                        keys.append(int(keyword))
                    for word in words:
                        if len(word) not in keys:
                            keys.append(len(word)) 
                else:
                    keys = self.generate_keys(keyword)
            
                # Перебор ключей
                for key in keys:
                    try:
                        if mode == "ASCII":
                            if cipher == "Caesar":
                                result = CaesarCipher.decrypt_ascii(
                                    input_text, int(key))
                            elif cipher == "Playfair":
                                result = PlayfairCipher.decrypt_ascii(
                                    input_text, key)
                            # elif cipher == "RSA":
                            #     char_table = "".join(chr(i).encode('latin1').decode('cp1251', errors='replace') for i in range(32, 256))
                            #     for rsa_p, rsa_q in prime_pairs_for_rsa:
                            #         try:
                            #             d, e = RSACipher.calculate_d_and_e(rsa_p, rsa_q)
                            #             result = RSACipher.decrypt_unicode(input_text, rsa_p, rsa_q, d, char_table)
                            #             results.append(
                            #                 f"CIPHER: {cipher.upper()} | DECRYPT | P: {rsa_p} | Q: {rsa_q} | E: {e} | D: {d} \nRESULT:\n{result}\n{'=' * 70}"
                            #             )
                            #         except Exception as e:
                            #             results.append(
                            #                 f"CIPHER: {cipher.upper()} | DECRYPT | P: {rsa_p} | Q: {rsa_q}\nERROR:\n{str(e)}\n{'=' * 70}"
                            #             )
                            elif cipher == "Vertical":
                                result = VerticalCipher.decrypt_ascii(
                                    input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.decrypt_ascii(
                                    input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.decrypt_ascii(
                                    input_text, key)
                            elif cipher == "Gronsfeld":
                                result = GronsfeldCipher.decrypt_ascii(
                                    input_text, key)
                            elif cipher == "Hill":
                                result = HillCipher.decrypt_ascii(
                                    input_text, key)         
                            elif cipher == "Algebra":
                                 obj = AlgebraOfMatrix(key)
                                 result = obj.decrypt(
                                    input_text)                           
                            else:
                                raise ValueError("Unsupported cipher!")
                        else:
                            if cipher == "Caesar":
                                result = CaesarCipher.decrypt_unicode(
                                    input_text, int(key))
                            elif cipher == "Playfair":
                                result = PlayfairCipher.decrypt_unicode(
                                    input_text, key)
                            elif cipher == "RSA":
                                if rsa_p and rsa_q and rsa_p.isdigit() and rsa_q.isdigit():
                                    rsa_p = int(rsa_p)
                                    rsa_q = int(rsa_q)
                                else:
                                    rsa_p = None
                                    rsa_q = None
                                if rsa_p is not None and rsa_q is not None:
                                    try:
                                        result = RSACipher.decrypt(input_text, rsa_p, rsa_q)
                                        if result:  # Проверяем, что result не пуст
                                            formatted_result = "\n\n".join(result)
                                            results.append(f"P: {rsa_p} | Q: {rsa_q}\nRESULT:\n{formatted_result}\n{'=' * 70}")
                                    except Exception as e:
                                        results.append(f"P: {rsa_p} | Q: {rsa_q}\nERROR:\n{str(e)}\n{'=' * 70}")
                                else:
                                    prime_pairs_for_rsa = self.generate_rsa_prime_pairs(11, 99, 100, 300)
                                    results.append(f"CIPHER: {cipher.upper()} | DECRYPT")
                                    for rsa_p, rsa_q in prime_pairs_for_rsa:
                                        try:
                                            result = RSACipher.decrypt(input_text, rsa_p, rsa_q)
                                            if result:  # Проверяем, что result не пуст
                                                formatted_result = "\n\n".join(result)
                                                results.append(f"P: {rsa_p} | Q: {rsa_q}\nRESULT:\n{formatted_result}\n{'=' * 70}")
                                        except Exception as e:
                                            results.append(f"P: {rsa_p} | Q: {rsa_q}\nERROR:\n{str(e)}\n{'=' * 70}")
                            elif cipher == "Vertical":
                                result = VerticalCipher.decrypt_unicode(
                                    input_text, key)
                            elif cipher == "Vijiner":
                                result = VigenereCipher.decrypt_unicode(
                                    input_text, key)
                            elif cipher == "DESS":
                                result = CustomDESCipher.decrypt_unicode(
                                    input_text, key)
                            elif cipher == "Gronsfeld":
                                result = GronsfeldCipher.decrypt_unicode(
                                    input_text, key)
                            elif cipher == "Algebra":
                                 obj = AlgebraOfMatrix(key)
                                 result = obj.decrypt(
                                    input_text)       
                            else:
                                raise ValueError("Unsupported cipher!")
                        # Добавляем успешный результат
                        results.append(
                            f"CIPHER: {cipher.upper()} | DECRYPT | KEYWORD: {
                                key}\nRESULT:\n{result}\n{'=' * 70}"
                        )
                    except Exception as e:
                        # Добавляем информацию об ошибке
                        results.append(
                            f"CIPHER: {cipher.upper()} | DECRYPT | KEYWORD: {
                                key}\nERROR:\n{str(e)}\n{'=' * 70}"
                        )
        except Exception as e:
            results.append(f"Error: {str(e)}")
        with open("results.txt", "w", encoding="utf8") as file:
            file.write("\n".join(results))
        # Вывод всех результатов в output_text
        self.output_text.delete("1.0", ctk.END)
        self.output_text.insert(ctk.END, "\n".join(results))
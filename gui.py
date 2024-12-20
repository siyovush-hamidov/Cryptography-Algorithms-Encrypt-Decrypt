import customtkinter as ctk
from ciphers import *


class CryptographyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cryptography Algorithms")
        self.geometry(f"{self.winfo_screenwidth()}x{
                      self.winfo_screenheight()}")
        # self.resizable(False, False)

        # Frame for cipher and encoding options
        options_frame = ctk.CTkFrame(self)
        options_frame.pack(pady=10, fill=ctk.X)

        self.cipher_combobox = ctk.CTkComboBox(options_frame, values=[
            "Atbash", "Caesar", "Playfair", "RSA", "Vertical", "Vijiner"])
        self.cipher_combobox.pack(side=ctk.LEFT, padx=5)
        self.cipher_combobox.set("Atbash")

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

        # Input Memo
        self.input_text = ctk.CTkTextbox(
            self, width=700, height=self.winfo_screenheight() // 2.5)
        self.input_text.pack(pady=5, fill=ctk.X)

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
            self, width=700, height=self.winfo_screenheight() // 2.5)
        self.output_text.pack(pady=5, fill=ctk.X)

    def encrypt(self):
        cipher = self.cipher_combobox.get()
        mode = self.radio_var.get()
        input_text = self.input_text.get("1.0", ctk.END).strip()
        keyword = self.keyword_entry.get().strip()
        try:
            if mode == "ASCII":
                if cipher == "Atbash":
                    output_text = AtbashCipher.reverse_message(input_text)
                elif cipher == "Caesar":
                    output_text = CaesarCipher.encrypt_ascii(
                        input_text, int(keyword))
                elif cipher == "Playfair":
                    output_text = PlayfairCipher.encrypt_ascii(
                        input_text, keyword)
                elif cipher == "RSA":
                    output_text = RSACipher.encrypt_ascii(input_text, keyword)
                elif cipher == "Vertical":
                    output_text = VerticalCipher.encrypt_ascii(input_text)
                elif cipher == "Vijiner":
                    output_text = VigenereCipher.encrypt_ascii(input_text, keyword)
                else:
                    raise ValueError("Unsupported cipher!")
            else:
                if cipher == "Atbash":
                    output_text = AtbashCipher.reverse_message(input_text)
                elif cipher == "Caesar":
                    output_text = CaesarCipher.encrypt_unicode(
                        input_text, int(keyword))
                elif cipher == "Playfair":
                    output_text = PlayfairCipher.encrypt_unicode(
                        input_text, keyword)
                elif cipher == "RSA":
                    output_text = RSACipher.encrypt_unicode(
                        input_text, keyword)
                elif cipher == "Vertical":
                    output_text = VerticalCipher.encrypt_unicode(input_text)
                else:
                    raise ValueError("Unsupported cipher!")
        except Exception as e:
            output_text = f"Error: {str(e)}"
        self.output_text.delete("1.0", ctk.END)
        self.output_text.insert(ctk.END, output_text)

    def decrypt(self):
        cipher = self.cipher_combobox.get()
        mode = self.radio_var.get()
        input_text = self.input_text.get("1.0", ctk.END).strip()
        keyword = self.keyword_entry.get().strip()
        try:
            if mode == "ASCII":
                if cipher == "Atbash":
                    output_text = AtbashCipher.reverse_message(input_text)
                elif cipher == "Caesar":
                    output_text = CaesarCipher.decrypt_ascii(
                        input_text, int(keyword))
                elif cipher == "Playfair":
                    output_text = PlayfairCipher.decrypt_ascii(
                        input_text, keyword)
                elif cipher == "RSA":
                    output_text = RSACipher.decrypt_ascii(input_text, keyword)
                elif cipher == "Vertical":
                    output_text = VerticalCipher.decrypt_ascii(input_text)
                elif cipher == "Vijiner":
                    output_text = VigenereCipher.decrypt_ascii(input_text, keyword)
                else:
                    raise ValueError("Unsupported cipher!")
            else:
                if cipher == "Atbash":
                    output_text = AtbashCipher.reverse_message(input_text)
                elif cipher == "Caesar":
                    output_text = CaesarCipher.decrypt_unicode(
                        input_text, int(keyword))
                elif cipher == "Playfair":
                    output_text = PlayfairCipher.decrypt_unicode(
                        input_text, keyword)
                elif cipher == "RSA":
                    output_text = RSACipher.decrypt_unicode(
                        input_text, keyword)
                elif cipher == "Vertical":
                    output_text = VerticalCipher.decrypt_unicode(input_text)
                else:
                    raise ValueError("Unsupported cipher!")
        except Exception as e:
            output_text = f"Error: {str(e)}"
        self.output_text.delete("1.0", ctk.END)
        self.output_text.insert(ctk.END, output_text)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = CryptographyApp()
    app.mainloop()

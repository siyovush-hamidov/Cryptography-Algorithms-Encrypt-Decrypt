class TestCipher:
    @staticmethod
    def strip(plain_message):
        plain_message = "".join(plain_message).replace('Зjx', 'ств')
        plain_message = "".join(plain_message).replace('ьГJ', 'чен') #K
        plain_message = "".join(plain_message).replace('5ІI', 'исл') #K
        plain_message = "".join(plain_message).replace('Аfѓ', 'кон')
        plain_message = "".join(plain_message).replace('¶{x', '  в')
        plain_message = "".join(plain_message).replace('Вdѓ', 'ммн')
        plain_message = "".join(plain_message).replace('Зg{', 'спе')
        plain_message = "".join(plain_message).replace('ЩXx', ' ав')
        plain_message = "".join(plain_message).replace('µlГёX™', ' ства')
        plain_message = "".join(plain_message).replace('    ъ+ц', '')
        plain_message = "".join(plain_message).replace('ѓЮ$', 'бов') #S
        plain_message = "".join(plain_message).replace('ЅuR', 'ви') #S        
        plain_message = "".join(plain_message).replace('сре ствасбора', 'средства сбора')
        return plain_message
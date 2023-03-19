""" Модуль, который содержит класс с константами
"""

import string


class Constants:
    # Все знаки препинания
    PUNCTUATION = list(string.punctuation)
    # Алфавиты
    RU_ALPHABET = [chr(sym) for sym in range(ord('а'), ord('я')+1)]
    EN_ALPHABET = list(string.ascii_lowercase)
    

    # Доступные языки
    RU_LANGUAGE = 'ru'
    EN_LANGUAGE = 'en'
    
    ALL_LANGUAGE = (RU_LANGUAGE, EN_LANGUAGE)
    
    # Словарь с сопоставлением языка и его алфавита
    DICT_LANGUAGE_ALPHABET = {
        RU_LANGUAGE: RU_ALPHABET,
        EN_LANGUAGE: EN_ALPHABET,
    }

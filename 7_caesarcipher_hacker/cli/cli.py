""" Модуль, который содержит класс, описывающий CLI для работы с шифром цезаря
"""

import os

from caesarcipher.caesarcipher import CaesarCipher, LanguageException
from caesarcipher.constants import Constants

from .cli_settings import CLISettings


class CLICaesarCipherHack:
    
    def _clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _get_input_language(self) -> None:
        """ Запрашивает у пользователя выбора языка для шифрования и 
            дешифрования текста
        """
        input_lang = None
        while not input_lang in Constants.ALL_LANGUAGE:
            self._clear_console()
            print('Все доступные языки: ' + ', '.join(Constants.ALL_LANGUAGE) + '\n')
            input_lang = input(CLISettings.INPUT_TEXT_FOR_GET_LANGUAGE)
        self._lang = input_lang

    def _get_input_hack_text(self) -> None:
        """ Запрашиваету  пользователя, текст который расшифровать
        """
        self._clear_console()
        text = input(CLISettings.INPUT_TEXT_FOR_HACK_DECODING)
        self._text = text

    def _hack_decode_text(self) -> None:
        """ Выполняем взлом текста, который зашифрован по методу цезаря
        """
        self._caesar.set_language(self._lang)
        for key in range(1, len(Constants.DICT_LANGUAGE_ALPHABET[self._lang])):
            self._caesar.set_key(key)
            self._all_result_text.append(f'Ключ #{key}. ' + self._caesar.decoding_text(self._text))

    def _pinting_result_text(self) -> None:
        """ Печатает на экран полученный текст в результате расшифрования
        """
        self._clear_console()
        print(CLISettings.PRINT_TEXT_RESULT + '\n')
        print('\n'.join(self._all_result_text))

    def __init__(self) -> None:
        self._all_result_text = []
        self._caesar = CaesarCipher()
    
    def start(self):
        # Получаем язык текста
        self._get_input_language()
        # Получаем текст, который необходимо взломать
        self._get_input_hack_text()
        # Кодируем/декодируем текст
        try:
            self._hack_decode_text()
        except LanguageException as e:
            self._clear_console()
            print(e)
        else:
            # Выводим полученный текст, на экран
            self._pinting_result_text()

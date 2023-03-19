""" Модуль, который содержит класс, описывающий CLI для работы с шифром цезаря
"""

import os

from caesarcipher.caesarcipher import CaesarCipher
from caesarcipher.constants import Constants

from .cli_settings import CLISettings


class CLICaesarCipher:
    
    def _clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _input_only_int(self, text_for_input: str, text_addition: str = '') -> int:
        """ Замена стандартному input, который на выходе дает только значения,
            которые можно преобразовать в int от пользователя

        Args:
            text_for_input (str): текст, который отображается в строчке при вводе
            text_addition (str): Допонительный текст, который необходим 
            пользователю для понимания. По умолчанию пустая строка.

        Returns:
            int: Введенное пользователем значение
        """
        value = None
        while not value and value != 0:
            try:
                self._clear_console()
                if len(text_addition) > 0:
                    print(text_addition)
                value = int(input('\n' + text_for_input))
            except ValueError:
                value = None
        return value
    
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
        
    def _get_input_encode_decode(self) -> None:
        """ Запрашивает у пользователя метод использования шифра цезаря.
            шифрования или дешифрования информации
        """
        f_encode = None
        while not f_encode in CLISettings.ALL_VALUE_FOR_ENCODING_DECODING_TEXT:
            text_addition = 'Доступные опции использования шифра цезаря: '
            for value, text in CLISettings.DICT_ALL_VALUE_ENCOD_DECOD_TEXT.items():
                text_addition += text + f'({value}), '
            f_encode = self._input_only_int(CLISettings.INPUT_TEXT_FOR_GET_FLAG_ENCODING, text_addition)
        self._f_encode = f_encode
        
    def _get_input_key_for_caesar(self) -> None:
        """ Запрашивает у пользователя, ключ шифрования 
        """
        key = None
        alphabet = Constants.DICT_LANGUAGE_ALPHABET[self._lang]
        while not key or not 0 < key < len(alphabet):
            text_addition = f'Ключ шифрования для выбранного языка составляет от 1 до {len(alphabet)-1}\n'
            key = self._input_only_int(CLISettings.INPUT_TEXT_FOR_GET_KEY, text_addition)
        self._key = key

    def _get_input_encode_decode_text(self) -> None:
        """ Запрашиваету  пользователя, текст который необходимо зашифровать или
            дешифровать
        """
        self._clear_console()
        text = input(CLISettings.INPUT_TEXT_FOR_ENCODING_DECODING)
        self._text = text

    def _encode_decode_text(self) -> None:
        """ Выполняем шифрования или дешифрования текст по методу цезаря,
            зависимости от заданного режима пользователем
        """
        self._caesar.set_language(self._lang)
        self._caesar.set_key(self._key)
        if self._f_encode == CLISettings.INPUT_VALUE_FOR_ENCODING_TEXT:
            self._result_text = self._caesar.encoding_text(self._text)
        elif self._f_encode == CLISettings.INPUT_VALUE_FOR_DECODING_TEXT:
            self._result_text = self._caesar.decoding_text(self._text)

    def _pinting_result_text(self) -> None:
        """ Печатает на экран полученный текст в результате шифрования или
            дешифрования
        """
        self._clear_console()
        print(CLISettings.PRINT_TEXT_RESULT + '\n')
        print(self._result_text)

    def __init__(self) -> None:
        self._caesar = CaesarCipher()
    
    def start(self):
        # Получаем язык текста
        self._get_input_language()
        # Получает действие с текстом
        self._get_input_encode_decode()
        # Получаем ключ шифрования
        self._get_input_key_for_caesar()
        # Получаем текст, который необходимо зашифровать/дешифровать
        self._get_input_encode_decode_text()
        # Кодируем/декодируем текст
        self._encode_decode_text()
        # Выводим полученный текст, на экран
        self._pinting_result_text()

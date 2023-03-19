""" Основной файл проекта, который содержит класс
"""

from constants import Constants


class CaesarCipher:
    
    def _set_current_alphabet(self) -> None:
        """ Устанавливает алфавит, зависимости от выбранного языка
        """
        self._alphabet = Constants.DICT_LANGUAGE_ALPHABET[self.current_language]
    
    def _check_key(self) -> None:
        """ Проверка ключа на валидность

        Raises:
            KeyCipher: Вызывается при не установке ключа или ухода его за ОДЗ
            ValueError: Если ключ не верного типа данных
        """
        if not self._key:
            raise KeyCipher('Ключ шифрования не установлен')
        if not isinstance(self._key, int):
            raise ValueError('Ключ шифрования имеет не верный тип данных')
        if not 0 <= self._key < len(Constants.DICT_LANGUAGE_ALPHABET[self.current_language]):
            raise KeyCipher('Ключ шифрования выходит за ОДЗ')
    
    def _check_symbol_in_alphabet(self, symbol: str) -> int | None:
        """ Определяем индекс заданного символа в словаре

        Args:
            symbol (str): Символ, который необходимо проверить

        Raises:
            LanguageException: Вызывается, при недопустимом символе для данного 
                языка

        Returns:
            int | None: Возвращает индекс заданного символа в алфавите или None,
                если заданный символ является знаком препинания
        """
        # Проверяем, что символ на знак препинания
        if symbol in Constants.PUNCTUATION:
            return None
        # Находим символ в алфавите
        try:
            ind_sym_in_alphabet = self._alphabet.index(symbol.lower())
        except ValueError:
            raise LanguageException(f'Символа "{symbol}" нет в алфавите "{self.current_language}" языка.')
        return ind_sym_in_alphabet
    
    def _get_new_index_symbol(self, curr_index: int, f_encode: bool) -> int:
        """ Метод рассчитывает новый индекс символа, для кодирования или
            декодирования, зависимости от флага

        Args:
            curr_index (int): Текущий индекс символа в алфавите
            f_encode (bool): Флаг кодирования или декодирования информации

        Returns:
            int: Новый индекс символа из алфавита
        """
        if f_encode:
            new_ind_sym = (curr_index+self._key)%len(self._alphabet)
        else:
            new_ind_sym = (curr_index-self._key)%len(self._alphabet)
        return new_ind_sym
    
    def _encode_decode_text(self, text: str, f_encode: bool) -> str:
        """ Метод кодирует или декодирует текст, зависимости от флага

        Args:
            text (str): Текст, который необходимо закодировать, или декодировать
            f_encode (bool): Флаг, который определяет, кодировать или 
                декодивароть информацию

        Returns:
            str: Закодированный или декодированный текст, зависимости от флага
        """
        # Устанавливаем алфавит
        self._set_current_alphabet()
        # Проверяем на наличие ключа
        self._check_key()
        # Выходной текст
        output = ''
        # Шифруем текст
        ind_sym = 0
        while ind_sym < len(text):
            # Определяем индекс в алфавите текущего символа
            ind_alphabet = self._check_symbol_in_alphabet(text[ind_sym])
            # Записываем новый символ
            if ind_alphabet:
                # Кодируем или декодируем информацию
                new_ind_sym = self._get_new_index_symbol(ind_alphabet, f_encode)
                new_symbol = self._alphabet[new_ind_sym]
            else:
                new_symbol = text[ind_sym]
            output += new_symbol
            # К следующему символу
            ind_sym += 1
        return output
    
    def __init__(self) -> None:
        # Ключ кодирования/декодирования
        self._key = None
        # Устанавлиавем язык
        self.set_language()
    
    def set_language(self, lang: str = Constants.RU_LANGUAGE) -> None:
        """ Метод установки языка кодирования/декодирования

        Args:
            lang (str): Язык, на котором будет кодирование и декодирование 
                информации. По умолчанию Constants.RU_LANGUAGE.

        Raises:
            LanguageException: Вызывается, при недопустимом выборе языка
        """
        # Проверяем доступен ли заданый язык
        if not lang in Constants.ALL_LANGUAGE:
            raise LanguageException('Выбранный язык недоступен')
        self.current_language = lang

    def set_key(self, key: int) -> None:
        """ Установить ключ кодирования/декодирования

        Args:
            key (int): ключи
        """
        self._key = key

    def encoding_text(self, text: str) -> str:
        """ Метод кодирования текста

        Args:
            text (str): Текст, который необходимо закодировать

        Returns:
            str: Закодированный текст
        """
        return self._encode_decode_text(text, True)
    
    def decoding_text(self, text: str) -> str:
        """ Декодирование текста

        Args:
            text (str): Текст, который необходимо декодировать

        Returns:
            str: Декодированный текст
        """
        return self._encode_decode_text(text, False)
        
        
class LanguageException(Exception):
    """ Исключение вызывается при недопустимом выборе языка, либо при отсутствии
        символа в алфавите
    """
    pass


class KeyCipher(Exception):
    """ Вызывается при не установленом ключе или при недопустимом ключе
    """

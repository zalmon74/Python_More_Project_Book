""" Файл описывает класс с настройками для CLI игры BLackJack
"""


class CLISettings:
    """ Класс с настройками для CLI игры BLackJack
    """
    # Текст для запроса данных у пользователя
    INPUT_TEXT_FOR_GET_LANGUAGE = 'Выберите один из доступных языков (Например: "ru"): '
    INPUT_TEXT_FOR_GET_FLAG_ENCODING = 'Введите цифру, для выбора использования метода цезаря (Например: "1"): '
    INPUT_TEXT_FOR_GET_KEY = 'Введите цифру из диапозона для выбора ключа (Например: "3"): '
    INPUT_TEXT_FOR_ENCODING_DECODING = 'Введите текст, который хотите зашифровать/дешифровать: '
    
    # Текст, который будет выводится перед результатом шифрования/дешифрования
    PRINT_TEXT_RESULT = 'Текст, который получился в результате шифрования/дешифрования'
    
    # Цифра, которая запрашивается у пользователя, чтобы метод использования
    # шифра цезаря воспринимался как шифрования информации
    INPUT_VALUE_FOR_ENCODING_TEXT = 1
    # Цифра, которая запрашивается у пользователя, чтобы метод использования
    # шифра цезаря воспринимался как дешифрования информации
    INPUT_VALUE_FOR_DECODING_TEXT = 2
    # Все опции использования шифра цезаря
    ALL_VALUE_FOR_ENCODING_DECODING_TEXT = (INPUT_VALUE_FOR_ENCODING_TEXT, INPUT_VALUE_FOR_DECODING_TEXT)
    DICT_ALL_VALUE_ENCOD_DECOD_TEXT = {
        INPUT_VALUE_FOR_ENCODING_TEXT: 'шифрования текста',
        INPUT_VALUE_FOR_DECODING_TEXT: 'Дешифрования текста',
    }

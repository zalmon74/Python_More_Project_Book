""" Файл, который содержит описание класса для игры Begals
"""

import random


class BegalsGame:
    """ Основной класс для игры
    """
    ## Настроечные константы
    # Количество символов в загаданном числе по умолчанию
    _COUNT_SYMBOLS_NUMBER = 3  
    # Максимальное количество попыток по умолчанию
    _MAX_COUNT_INPUT_VALUE = 10 
    
    ## Вспомогательные константы
    _NAME_GAME = 'Бегалс'
    
    ## Константы для сообщений на экране
    # Если цифра угадана и его местоположение
    _PRINT_CORRECT_NUMBER_CORRECT_PLACE = 'FERMI'
    # Если цифра угадана, а местоположение нет
    _PRINT_CORRECT_NUMBER_WRONG_PLACE = 'PICO'
    # Если в заданном значение нет правильных цифр
    _PRINT_WRONG_NUMBER = 'BEGALS'
    
    def _print_hello_game(self):
        """ Метод печати приветствия в игре
        """
        print(f'\nДобро пожаловать в игру {BegalsGame._NAME_GAME}!\n')
        print(f'Суть игры заключается в угадывании заданного числа комьпютером,'+
              f'состоящим из {self.__count_symbols_number} символов по подсказкам.'+
              f'На это у вас будет {self.__max_count_input_value} попыток.')
    
    def _print_help(self):
        """ Метод печати вспомогательной информации по игре
        """
        print('\nПосле того как копьютер загадает число, вам будет предоставлена'+
              ' возможность попробовать угадать задагаднное число. После ввода,'+
              ' копьютер даст вам одну из 3х подсказок, если число не было угадано.'
             )
        print('Возможные подсказки:')
        print(f'{BegalsGame._PRINT_CORRECT_NUMBER_CORRECT_PLACE}',
              '- Вы угадали число и его местоположение;')
        print(f'{BegalsGame._PRINT_CORRECT_NUMBER_WRONG_PLACE}',
              '- Вы угадали число, но не угадали его местоположение;')
        print(f'{BegalsGame._PRINT_WRONG_NUMBER}',
              '- В заданном числе нет загаданных цифр.')
        
    def _print_hidden_value(self):
        """ Метод вывода на экран загаданного компьютером числа
        """
        print(f'Копьютер загадал число: {self._hidden_value}.')
    
    def _print_win_str(self):
        """ Метод печати строки при угадывании числа
        """
        print('Поздравляю, вы угадали число и победили')

    def _get_input_value(self):
        """ Метод получения числа от пользователя
        """
        self._input_value = input(f'Введите число, которое состоит из {self.__count_symbols_number}'+
                                  ' цифр: ')
    
    def _generate_hidden_value(self):
        """ Метод генерации числа
        """
        # Генерируем загаданное число посимвольно
        lst = []
        for _ in range(self.__count_symbols_number):
            lst.append(str(random.randint(0, 9)))
        # Формируем из сиволов число
        self._hidden_value = ''.join(lst)
    
    def _check_input_value(self):
        """ Метод сверят введенное число с загаданным. Если число угадано выдает
            True, иначе False.
        """
        output = self._input_value == self._hidden_value
        # Если числа не равны, нужно сообщить пользователю одну из возможных
        # подсказак
        if not output:
            self._check_symbols_input_value()    
        return output
    
    def _check_symbols_input_value(self):
        """ Метод проверяет цифры в введенном числе, а также печатает
            подсказку для пользователя
        """
        # Перебираем каждую цифру и сверяем с загаданным числом
        if len(self._input_value) == len(self._hidden_value):
            # Флаг для определения вывода подсказки
            f_print = False 
            for ind in range(len(self._input_value)):
                if (self._input_value[ind] in self._hidden_value) and\
                   (self._input_value[ind] == self._hidden_value[ind]):
                    f_print = True
                    if ind != len(self._input_value)-1:
                        print(f'{BegalsGame._PRINT_CORRECT_NUMBER_CORRECT_PLACE}', end=' ')
                    else:
                        print(f'{BegalsGame._PRINT_CORRECT_NUMBER_CORRECT_PLACE}')
                elif (self._input_value[ind] in self._hidden_value) and\
                     (self._input_value[ind] != self._hidden_value[ind]):
                    f_print = True
                    if ind != len(self._input_value)-1:
                        print(f'{BegalsGame._PRINT_CORRECT_NUMBER_WRONG_PLACE}', end=' ')
                    else:
                        print(f'{BegalsGame._PRINT_CORRECT_NUMBER_WRONG_PLACE}')
                    
            if not f_print:
                print(f'{BegalsGame._PRINT_WRONG_NUMBER}') 
        else:
            print(f'{BegalsGame._PRINT_WRONG_NUMBER}') 
    
    def __init__(self, count_symbs_number: int = _COUNT_SYMBOLS_NUMBER,
                 max_count_input_value: int = _MAX_COUNT_INPUT_VALUE):
        """ Конструктор
        
        :param: count_symbs_number (int) - количество цифр в загаданном числе
        :param: count_max_input_value (int) - максимальное количество попыток,
                    чтобы угадать число
        """
        # Настроечный параметр, который указывает на количество цифр в 
        # загаданном числе
        self.__count_symbols_number = count_symbs_number
        # Настроечный параметр, который указывает на максимальное количество 
        # попыток, чтобы угадать значение
        self.__max_count_input_value = max_count_input_value
        
        # Поля, для работы с загаданным числом
        # Загаданное значение
        self._hidden_value = None  
        
        # Поля для работы с веденным значением пользователя
        # Введенное значение
        self._input_value = None  
    
    # Сеттеры
    def set_count_symbols_number(self, input_value: int):
        """ Сеттер для установки количества цифр в загаданном числе

        :param: input_value (int) - количества цифр в загаданном числе
        """
        self.__count_symbols_number = input_value
    
    def set_count_max_input_value(self, input_value: int):
        """ Сеттер для установки количества цифр в загаданном числе

        :param: input_value (int) - количества цифр в загаданном числе
        """
        self.__max_count_input_value = input_value
    
    def start_game(self):
        """ Метод запуска игры
        """
        # Выводим на экран приветствие пользователя и правила игры
        self._print_hello_game()
        self._print_help()
        
        # Формируем загаданное число
        self._generate_hidden_value()
        
        for num_input in range(self.__max_count_input_value):
            self._get_input_value()
            f_guessed = self._check_input_value()
            if f_guessed:
                self._print_win_str()
                break;
                
        
        
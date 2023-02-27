""" Файл описывает основной класс CLI для игры BlackJack
"""

import os
from msvcrt import getch
from typing import Callable

from .cli_settings import CLISettings
from blackjack import BlackJack, Constants
from players import Player


class CLIBlackJack:
    """ Класс, описывающий CLI, для игры BlackJack
    """
    
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
        while not value:
            try:
                MenuCLI.clear_console()
                if len(text_addition) > 0:
                    print(text_addition)
                value = int(input('\n' + text_for_input))
            except ValueError:
                value = None
        return value
        
    
    def _get_input_count_peoples(self) -> int:
        """ Метод запрашивает у пользователя сколько игроков будет в данной игре

        Returns:
            int: Количество игроков, которое ввел пользователь
        """
        text_addition = f'Количество людей не должно превышать {Constants.MAX_PLAYERS}'
        count_players = None
        while not count_players:
            count_players = self._input_only_int(CLISettings.TEXT_FOR_INPUT_COUNT_PEOPLES, text_addition)
            # Количество игроков не может иметь отрицательное значение и 
            # не должно превышать максимально допустимое значение игроков
            if 0 > count_players or count_players > Constants.MAX_PLAYERS:
                count_players = None
        return count_players
    
    def _create_object_players(self, num_player: int) -> Player:
        """ Создает объект типа "Player" с настройками, которые введт 
            пользователь

        Args:
            num_player (int): Порядковый номер игрока

        Returns:
            Player: Созданный объект
        """
        additional_text = f'Игрок #{num_player}. '
        # Запрашиваем имя игрока 
        MenuCLI.clear_console()
        print(additional_text)
        name_player = input(CLISettings.TEXT_FOR_INPUT_NAME_PLAYER)
        additional_text += f'Имя игрока: {name_player}'
        # Запрашиваем количество денег у игрока
        count_meney = self._input_only_int(CLISettings.TEXT_FOR_INPUT_COUNT_MONEY, additional_text)
        return Player(name_player, count_meney)
    
    def _create_list_objects_players(self, count_players: int) -> list[Player]:
        """ Метод создает список с объектами, которые описывают каждого игрока

        Args:
            count_players (int): Количество игроков, которое необходимо создать

        Returns:
            list[Player]: Созданный список
        """
        output = []
        for ind_player in range(count_players):
            # +1 - чтобы нумерация игроков шла с 1 (для удобности клиентов)
            output.append(self._create_object_players(ind_player+1))
        return output
    
    def _add_players(self) -> None:
        # Определяем количество игроков
        count_players = self._get_input_count_peoples()
        print(self._create_list_objects_players(count_players))
        getch()
    
    def _start_game(self) -> None:
        """ Метод описывает взаимодействие игры и пользователя
        """
        self._add_players()
    
    def _get_rulles_for_game(self) -> None:
        """ Метод отображает на экране правила игры
        """
        MenuCLI.clear_console()
        print(CLISettings.TEXT_RULES)
        print('\n' + CLISettings.TEXT_FOR_INPUT_WITH_RULES, end='')
        getch()
    
    def _create_main_menu(self) -> None:
        """ Метод создает главное меню
        """
        fields = {
            'Начать игру': self._start_game,
            'Правила': self._get_rulles_for_game,
            'Выйти': MenuCLI.exit_menu,
        }
        self._main_menu = MenuCLI(fields)
    
    def __init__(self) -> None:
        self._game = BlackJack()
        
        self._create_main_menu()
    
    def start(self):
        self._main_menu.start_menu()
    

class MenuCLI:
    """ Класс описывает меню
    """
    
    def exit_menu():
        """ Функция для вызова исключения выхода из меню
        """
        raise _ExitMenu
    
    def clear_console() -> None:
        """ Отчищает экран консоли
        """
        os.system('cls' if os.name=='nt' else 'clear')
    
    # Приватные методы

    def _print_menu(self) -> None:
        """ Печатает меню в консоль
        """
        for ind, name in enumerate(self._menu_dict.keys(), 1):
            print(f'{ind}. {name} ', flush=False)
    
    def _input_num_field_menu(self) -> None:
        """ Метод запрашивает у пользователя номер поля из меню
        """
        try:
            val = int(input('\n' + CLISettings.TEXT_FOR_INPUT_FIELD))
            if 0 < val <= self._len_menu:
                for num, field in enumerate(self._menu_dict.items(), 1):
                    name, func = field
                    if num == val and isinstance(func, Callable):
                        func()
        except ValueError:
            return None
    
    def __init__(self, menu: dict[str, Callable] = dict()) -> None:
        """ Конструктор

        Args:
            menu (dict[str, Callable]): словарь, который содержит пункты меню
            и функция, которая будет вызваться при выборе данного пунка
        """
        self._menu_dict = menu
        self._len_menu = len(menu)
        
    def add_fields(self, fields: dict[str, Callable]) -> None:
        """ Метод позволяет добавить в меню 

        Args:
            fields (dict[str, Callable]): Словарь с полями, которые необходимо
            добавить в меню
        """
        for name, func in fields.items():
            self._menu_dict[name] = func
        self._len_menu = len(self._menu_dict)
            
    def start_menu(self) -> None:
        """ Запускает консольное меню
        """
        f_inf = True
        while f_inf:
            MenuCLI.clear_console()
            self._print_menu()
            try:
                self._input_num_field_menu()
            except _ExitMenu:
                f_inf = False
            

class _ExitMenu(Exception):
    """ Исключение, которое позвояет выйти из меню
    """
    pass
""" Файл описывает основной класс CLI для игры BlackJack
"""

import os
from typing import Callable

from .cli_settings import CLISettings


class CLIBlackJack:
    """ Класс, описывающий CLI, для игры BlackJack
    """
    pass
    

class MenuCLI:
    """ Класс описывает меню
    """
    
    def exit_menu():
        """ Функция для вызова исключения выхода из меню
        """
        raise _ExitMenu
    
    # Приватные методы
    
    def _clear_console(self) -> None:
        """ Отчищает экран консоли
        """
        os.system('cls' if os.name=='nt' else 'clear')

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
            self._clear_console()
            self._print_menu()
            try:
                self._input_num_field_menu()
            except _ExitMenu:
                f_inf = False
            

class _ExitMenu(Exception):
    """ Исключение, которое позвояет выйти из меню
    """
    pass
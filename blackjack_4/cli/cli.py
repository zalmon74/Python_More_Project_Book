""" Файл описывает основной класс CLI для игры BlackJack
"""

import os
from msvcrt import getch
from typing import Callable
from time import sleep

from .cli_settings import CLISettings
from blackjack import BlackJack, Constants
from players import Player
from card_deck import list_card_2_str_for_print


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
            player = self._create_object_players(ind_player+1)
            # Изабавляем от повторений пользователей в игре
            while player in output:
                print('\n' + CLISettings.TEXT_FOR_REPEAT_PLAYER_NAME)
                getch()
                player = self._create_object_players(ind_player+1)
            output.append(player)
        return output
    
    def _get_bet_player(self, num_player: int, name_player: str, max_bet: int) -> int:
        """ Запрашивает ставку у одного игрока

        Args:
            num_player (int): Порядковый номер игрока
            name_player (str): Имя игрока
            max_bet (int): Максимальная ставка, которую игрок может поставить
        
        Returns:
            int: _description_
        """
        text_additional = f'Игрок #{num_player}. Имя игрока: {name_player}. Максимальная ставка: {max_bet}.'
        bet = None
        while not bet:
            bet = self._input_only_int(CLISettings.TEXT_FOR_INPUT_BET, text_additional)
            # Количество игроков не может иметь отрицательное значение и 
            # не должно превышать максимально допустимое значение игроков
            if 0 > bet or bet > max_bet:
                bet = None
        return bet
    
    def _get_bet_for_all_players(self) -> list[int]:
        """ Запрашивает у каждого игрока ставку для игры

        Returns:
            list[int]: Возвращает список, который содержит ставку для каждого 
            игрока
        """
        bets = []
        for ind in range(len(self._all_players)):
            player = self._all_players[ind]
            bets.append(self._get_bet_player(ind+1, player.name, player.get_count_money()))
        self._bets_players = bets
    
    def _add_players_for_game(self) -> None:
        """ Добавляем объекты с игроками в игру с их ставками
        """
        for player, bet in zip(self._all_players, self._bets_players):
            # Перед добавлением, очищаем все карты у игрока
            player.clear_cards()
            self._game.add_player_for_game(player, bet)
    
    def _add_players(self) -> None:
        """ Метод добавляет игроков для игры
        """
        # Определяем количество игроков
        count_players = self._get_input_count_peoples()
        # Получаем имена игроков, количество их денег и ставки
        self._all_players = self._create_list_objects_players(count_players)
    
    def _party_game_for_player(self, num_player: int) -> None:
        """ Игровая партия в игру для одного игрока

        Args:
            num_player (int): Порядковый номер игрока
        """
        current_player, _ = self._game.get_current_player()
        dealer = self._game.get_dealer()
        while current_player == self._game.get_current_player()[0]:
            additional_text  = f'Карты дилера:\n' + list_card_2_str_for_print(dealer.get_all_cards()) + '\n'
            additional_text += f'Карты игрока #{num_player}. Имя игрока: {current_player.name}. Текущее кол-во очков: {current_player.get_points()}.\n'
            additional_text += list_card_2_str_for_print(current_player.get_all_cards()) + '\n'
            if current_player.get_points() < Constants.COUNT_POINTS_FOR_WIN:
                self._game_player_menu.start_menu(additional_text)
            else:
                self._game_player_menu_lot.start_menu(additional_text)
    
    def _party_game_for_dealer(self) -> None:
        """ Метод описывает игровую партию для дилера
        """
        def _print_text():
            MenuCLI.clear_console()
            text  = f'У дилера текущее кол-во очков: {dealer.get_points()}. '
            text += f'Карты дилера: \n' + list_card_2_str_for_print(dealer.get_all_cards())
            text += '\nЧтобы продолжить, нажмите любую кнопку'    
            print(text)
        
        dealer = self._game.get_dealer()
        while dealer.get_points() < Constants.COUNT_POINTS_FOR_STOP_TAKE_CARDS_DEALER:
            _print_text()
            getch()
            self._game.add_card_for_current_player()
        _print_text()
        getch()
        
    def _results_party_game(self) -> None:
        """ Подводит итоги игры и выводит результаты на экран
        """
        f_stop, results_party = self._game.check_stop_game()
        for player, f_win in results_party.items():
            text_for_print = f'Игрок {player.name} '
            if f_win is None:
                text_for_print += f'ничья. '
            elif f_win:
                text_for_print += f'выиграл. '
            else:
                text_for_print += f'проиграл. '
            text_for_print += f'Баланс составляет: {player.get_count_money()}.\n\n'
            text_for_print += 'Нажмите кнопку, чтобы продолжить'
            MenuCLI.clear_console()
            print(text_for_print)
            getch()
    
    def _start_party_game(self) -> None:
        """ Метод запускает одну партию игры 
        """
        # Создаем объект с игрой
        self._game = BlackJack()
        # Создаем меню для игры
        self._create_game_player_menu()
        self._create_game_player_menu_lot()
        # Запрашиваем ставки игроков и добавляем их в игру
        self._get_bet_for_all_players()
        # Добавляем игроков в игру
        self._add_players_for_game()
        # Начинаем игру
        self._game.start()
        # Игровая партия для игроков
        for ind_player in range(len(self._all_players)):
            self._party_game_for_player(ind_player+1)
        # Игровая партия для дилера
        self._party_game_for_dealer()
        # Подводим итоги
        self._results_party_game()
        
        
    def _start_game(self) -> None:
        """ Метод описывает взаимодействие игры и пользователя
        """
        # Добавляем игроков в игру
        self._add_players()
        # Запускаем игровую партию
        self._start_party_game()
        # Выводим меню после партии игры
        self._game_again_play_menu.start_menu()
    
    def _add_card_for_current_player_in_game_menu(self) -> None:
        """ Метод добавляет карту для текущего игрока. Метод нужен для меню
            игрока при выборе добавить "CLISettings.TEXT_FOR_ADD_CARD_PLAYER"
        """
        self._game.add_card_for_current_player()
        MenuCLI.exit_menu()
        
    def _next_player_in_game_menu(self):
        """ Метод позволяет перейсти к следующему игроку. Метод нужен для меню
            игрока при выборе "CLISettings.TEXT_FOR_ENOUGH_CARDS_PLAYER"
        """
        self._game.next_player()
        MenuCLI.exit_menu()
    
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
    
    def _create_game_player_menu(self) -> None:
        """ Метод создает меню выбора для игрока при взятии карт
        """
        fields = {
            CLISettings.TEXT_FOR_ADD_CARD_PLAYER: self._add_card_for_current_player_in_game_menu,
            CLISettings.TEXT_FOR_ENOUGH_CARDS_PLAYER: self._next_player_in_game_menu,
        }
        self._game_player_menu = MenuCLI(fields)
    
    def _create_game_player_menu_lot(self) -> None:
        """ Метод создает меню выбора игрока при взятии карт, когда у игрока
            перебор по очкам
        """
        fields = {
            CLISettings.TEXT_FOR_ENOUGH_CARDS_PLAYER: self._next_player_in_game_menu,
        }
        self._game_player_menu_lot = MenuCLI(fields)
    
    def _create_agaim_play_menu(self) -> None:
        """ Метод создает меню после игры, которое предлагает начать новую партию
            или выйти в главное меню
        """
        fields = {
            CLISettings.TEXT_FOR_PLAY_AGAIN : self._start_party_game,
            CLISettings.TEXT_FOR_EXIT_IN_MAIN_MENU: MenuCLI.exit_menu,
        }
        self._game_again_play_menu = MenuCLI(fields)
        
    def __init__(self) -> None:
        self._create_main_menu()
        self._create_agaim_play_menu()
    
    def start(self) -> None:
        """ Запуск CLI для игры BlackJack
        """
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
            
    def start_menu(self, additional_text: str = '') -> None:
        """ Запускает консольное меню
        
        Args:
            addition_text (str): Дополнительный текст, который необходимо 
            вывести перед меню
        """
        f_inf = True
        while f_inf:
            MenuCLI.clear_console()
            if len(additional_text):
                print(additional_text + '\n')
            self._print_menu()
            try:
                self._input_num_field_menu()
            except _ExitMenu:
                f_inf = False
            

class _ExitMenu(Exception):
    """ Исключение, которое позвояет выйти из меню
    """
    pass
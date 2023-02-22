""" Файл описывает игральные карты и колоду
"""

from dataclasses import dataclass
from random import shuffle

from constants import Constants


def list_card_2_str_for_print(lst_cards: list, sep: str = '\t') -> str:
    """ Функция генерирует строку, которая отображает красивую форму карт в 
        консоли

    Args:
        lst_cards (list): Список с картами, которые необходимо превратить в строку

    Returns:
        str: Строка, которая красиво отображает карты в консоле
    """
    output = ''
    for num_str in range(4):
        for card in lst_cards:
            if num_str == 0:
                output += ' ___'
            if num_str == 1:
                if len(card.name) == 2:
                    output += f'|{card.name} |'
                else:
                    output += f'|{card.name}  |'
            if num_str == 2:
                output += f'| {card.suit} |'
            if num_str == 3:
                if len(card.name) == 2:
                    output += f'|_{card.name}|'
                else:
                    output += f'|__{card.name}|'
            output += sep
        output += '\n'
    return output

@dataclass(unsafe_hash=True)
class Card:
    """ Класс описывает одну карту из колоды
    
        Если у карты нет альтернативного количества очков, то данное поле 
        заполняется таким же значением, как и обычное количество очков
    """
    name: str  # Имя карты
    suit: str  # Масть карты
    points: int  # Количество очков, которое приносит карта
    alter_points: int  # Альтернативное количество очков, которое приносит карта (необходимо для туза)
    
    def __str__(self) -> str:
        return list_card_2_str_for_print([self,])
    

class CardDeck:
    """ Описывает игральную колоду карт
    """
    
    def _generate_all_cards(self):
        """ Метод формирует список со всеми существующими картами
        """
        self._all_cards = set()
        for name, points in Constants.DICT_ALL_NAME_CARDS.items():
            for suit in Constants.ALL_SUIT_FOR_GAME:
                self._all_cards.add(Card(name, suit, points[0], points[1]))
    
    def _generate_deck_for_game(self):
        """ Метод генерирует кортеж с играбельной колодой
        """
        self._deck = list(self._all_cards)
        shuffle(self._deck)
        
    def __init__(self):
        self._generate_all_cards()
        self._generate_deck_for_game()
    
    def start_new_deck(self) -> None:
        """ Метод позволяет начать новую колоду
        """
        self._generate_deck_for_game()
    
    def shuffle(self, count: int = 1) -> None:
        """ Метод позволяет перемешать колоду "count" раз        

        Args:
            count (int): Количество перемешиваний. По умолчанию 1.
        """
        for _ in range(count):
            shuffle(self._deck)
    
    def get_card(self) -> Card:
        """ Метод позволяет получить следующую карту из колоды

        Returns:
            Card: Объект, который описывает карту из колоды
        """
        return self._deck.pop()

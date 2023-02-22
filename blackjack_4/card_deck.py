""" Файл описывает игральные карты и колоду
"""

from dataclasses import dataclass

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

@dataclass
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
    

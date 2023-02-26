""" Файл описывает класс игрока
"""

from card_deck import Card
from constants import Constants


class Player:
    """ Класс игрока для игры в BlackJack
    """
    
    # Дандеры
    
    def __init__(self, name: str = 'Anonym', money: int = 1000) -> None:
        # Имя игрока
        self.name = name
        # Количество денег
        self._money = money
        # Карты на руке у игрока
        self._cards = []
       
    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name
    
    # Геттеры   
     
    def get_all_cards(self) -> list[Card]:
        """ Возвращает список с картами, которые имеются на руке у игрока

        Returns:
            list[Card]: список с картами, которые имеются на руке у игрока
        """
        return self._cards[:]

    def get_points(self) -> int:
        """ Позволяет получить количество очков на руке у игрока

        Returns:
            int: Возвращает количество очков на руке игрока
        """
        output = 0
        if len(self._cards) > 0:
            output = get_count_points_for_cards(self._cards)
        return output

    def get_count_money(self) -> int:
        """ Позволяет получить текущее количество денег у игрока

        Returns:
            int: Текущее количество денег
        """
        return self._money
    
    # Сеттеры
    
    def set_card(self, card: Card | list[Card]) -> None:
        """ Добавляем заданные карты в руку игрока

        Args:
            card (Card | list[Card]): Карта или карты, которые необходимо
            добавить игроку

        Raises:
            ValueError: Вызывается, если в качестве входных данных задан объект,
            который не является экземпляром Card или списоком, который содержит
            экземпляры класса Card, а также если данный список имеет нулевую
            длину
        """
        if isinstance(card, Card):
            self._cards.append(card)
        elif isinstance(card, list) and (len(card) > 0 and isinstance(card[0], Card)):
            self._cards.extend(card)
        else:
            raise ValueError(f'Входные данные "card" не являеются объектом типа "Card", или list[Card], или list[Card] пустой.')
    
    # Всмопогательные методы
    def change_count_money(self, count_change: int) -> None:
        """ Метод позволяет имзенить количество денег игрока на заданное
            количество (count_change)

        Args:
            count_change (int): Количество денег, на которое необходимо
            изменить у игрока

        Raises:
            ValueError: вызвается, если у игрока отнимается денег больше, чем
            у него есть
        """
        if count_change < 0 and abs(count_change) > self._money:
            raise ValueError('У игрока нет столько денег')
        else:            
            self._money += count_change
    
        
def get_count_points_for_cards(cards: Card | list[Card], f_alter_points: bool = False) -> int:
    """ Позволяет получить количество очков на руке у игрока

    Args:
        cards (Card | list[Card]): Экземпляр класса Card или список с объектами
        типа Card, у которых необходимо посчитать количество очков
        f_alter_points (bool): Флаг, который говорит считать карты по 
        альтернативным очкам или по обычным

    Raises:
        ValueError: Вызывается, если в качестве входных данных задан объект,
        который не является экземпляром Card или списоком, который содержит
        экземпляры класса Card, а также если данный список имеет нулевую
        длину
    
    Returns:
        int: Сумма очков у заданных карт
    """
    output = 0
    if isinstance(cards, Card):
        if f_alter_points:
            output += cards.alter_points
        else:
            output += cards.points
    if isinstance(cards, list) and (len(cards) > 0 and isinstance(cards[0], Card)):
        if f_alter_points:
            output += sum([card.points for card in cards])
        else:
            output += sum([card.alter_points for card in cards])
    else:
        raise ValueError(f'Входные данные "cards" не являеются объектом типа "Card", или list[Card], или list[Card] пустой.')
    # Если сумма карт больше "COUNT_POINTS_FOR_WIN", тогда некоторые карты имеют
    # альтернативное количество очков, поэтому необходио пересчитать с
    # альтернативными очками
    if output > Constants.COUNT_POINTS_FOR_WIN and not f_alter_points:
        output = get_count_points_for_cards(cards, True)
    return output
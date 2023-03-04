""" Файл, который содержит описание класса для игры BlackJack
"""

from constants import Constants
from players import Player
from card_deck import Card, CardDeck


class BlackJack:
    """ Класс, который описывает игру BlackJack
    
        Цель — обыграть дилера (крупье). Набрать больше очков, чем у дилера, но не больше 21. 
        Значения очков каждой карты: от двойки до десятки — от 2 до 10 соответственно, у туза — 1 или 11 (11 пока общая сумма не больше 21, далее 1), у т. н. картинок (король, дама, валет) — 10.
        Если у игрока и дилера число очков на руках равное, то такая ситуация называется «ровно» (пуш, англ. push). В такой ситуации все остаются при своих ставках, никто не выигрывает и проигрывает.
        Игроки до раздачи карт делают ставки, кладя фишки на соответствующие поля игрового стола. 
        После того, как первая карта сдана, игрокам запрещается делать ставки и прикасаться к своим фишкам.
        Дилер раздаёт карты: по две карты каждому игроку, себе раздаёт одну карту. Все карты открываются сразу (видны и дилеру, и игроку).
        Если у игрока сразу после раздачи набралось 21 очко (то есть у игрока туз и десятиочковая карта), то такая ситуация и называется блек-джек. В таком случае игроку сразу выплачивается выигрыш 3 к 2 (то есть в 1,5 раза превышающий его ставку). Исключение составляют случаи, когда дилеру первой картой (открытой) попадается 10, картинка или туз. В этом случае существует вероятность, что у дилера также будет блек-джек, поэтому игроку с блек-джеком предлагается либо взять выигрыш 1 к 1 (только если первая карта дилера — туз), либо дождаться окончания конца игры (и в случае, если у дилера не блек-джек, получить выигрыш 3 к 2).
        Далее игрокам, у которых не блек-джек, предлагается на выбор либо взять ещё карту (в таком случае игрок должен сказать дилеру «карту» или «ещё», англ. hit me), либо остаться при тех картах (и той сумме очков), которые у него на руке (в этом случае игрок должен сказать дилеру «достаточно» или «хватит»).
        Как правило, если у игрока после взятия новой карты в сумме получается 21, дилер не спрашивает его больше и переходит к следующему игроку.
        Если у игрока после взятия новой карты сумма очков превысит 21, то такая ситуация называется «перебор». Дилер произносит «много» и снимает ставку игрока в пользу казино.
        Если у дилера в первых двух картах набирается 21 очко (блек-джек), то все игроки (кроме тех, у кого тоже блек-джек), проигрывают. Те, у которых блек-джек, остаются при своих ставках, если они ранее не выбрали взять выигрыш 1 к 1 или если не застраховали свою комбинацию от блек-джека.
        После того, как все игроки завершили брать карты, дилер говорит «себе» и раздаёт карты себе. Общее правило блек-джека состоит в том, что дилер обязан остановиться, как только наберёт 17 очков или выше, и обязан брать, пока не достигнет (даже если у всех не перебравших меньше очков).
        При окончательном подсчёте очков в конце раунда карты остальных игроков для вас значения не имеют, игра ведётся только против дилера, то есть сравниваются карты только игрока и дилера, карты и ставки параллельных игроков не учитываются.
    """
    
    # Приватыне методы
    
    def _generator_for_game(self) -> None:
        """ Данный генератор необходим для выбора игры с определенным игроком
        """
        while self._ind_current_player < len(self._players):
            yield
            self._ind_current_player += 1
    
    def _scoring(self) -> dict[Player, bool]:
        """ Метод подводит итоги, распределяет выигрышь, а также
            возвращает словарь, который в качестве ключей содержит
            объект типа "Player", а данных флаг победы (False - проиграл,
            True - победил)            
        
        Returns:
            dict[Player, bool]: Словарь с результатами для каждого игрока,
            который в качестве ключей содержит объект типа "Player", а данных
            флаг победы (False - проиграл, True - победил, None - ничья)   
        """
        results = self.get_results()
        for player, f_win in results.items():
            # Если игрок победил, то прибавляем ему деньги, иначе отнимаем
            if f_win is None:
                continue
            elif f_win:
                player.change_count_money(self._bets[player])
                self._dealer.change_count_money(0-self._bets[player])
            else:
                player.change_count_money(0-self._bets[player])
                self._dealer.change_count_money(self._bets[player])
        return results
    
    # Дандеры 
    
    def __init__(self) -> None:
        self.clear()
        
    # Геттеры    
    
    def get_count_players(self) -> int:
        """ Позволяет получить текущее количество игроков
        
        Returns:
            int: Текущее количество игроков
        """
        return len(self._players)

    def get_dealer(self) -> Player:
        """ Возвращает экземпляр класса Playr, который описывает дилера (крупье)

        Returns:
            Player: Объект, который описывает дилера (крупье)
        """
        return self._dealer
    
    def get_current_player(self) -> tuple[Player, int]:
        """ Возвращает текущего игрока и его индекс

        Returns:
            tuple[Player, int]: Возвращает объект с пользователем и его номер (индекс)
        """
        if self._ind_current_player < len(self._players):
            output = self._players[self._ind_current_player]
            output = (output, self._ind_current_player)
        else:
            output = self._dealer
            output = (output, None)
        return output
    
    def get_all_cards_for_current_player(self) -> list[Card]:
        """ Возвращает список с картами для текущего игрока
        
        Returns:
            list[Card]: Список, который содержит карты текущего игрока
        """
        if self._ind_current_player < len(self._players):
            output = self._players[self._ind_current_player].get_all_cards()
        else:
            output = self._dealer.get_all_cards()
        return output
    
    def get_count_points_for_current_player(self) -> int:
        """ Возвращает количество очков для текущего игрока

        Returns:
            int: Количество очков текущего игрока
        """
        if self._ind_current_player < len(self._players):
            output = self._players[self._ind_current_player].get_points()
        else:
            output = self._dealer.get_points()
        return output
    
    def get_results(self) -> dict[Player, bool]:
        """ Метод возвращает словарь, который в качестве ключей содержит
            объект типа "Player", а данных флаг победы (False - проиграл,
            True - победил)            
        
        Returns:
            dict[Player, bool]: Словарь с результатами для каждого игрока,
            который в качестве ключей содержит объект типа "Player", а данных
            флаг победы (False - проиграл, True - победил)            
        """
        output = dict()
        for player in self._players:
            if player.get_points() == self._dealer.get_points():
                result = None
            elif player.get_points() > self._dealer.get_points() and \
               player.get_points() <= Constants.COUNT_POINTS_FOR_WIN:
                result = True
            elif player.get_points() <= Constants.COUNT_POINTS_FOR_WIN and \
                 self._dealer.get_points() > Constants.COUNT_POINTS_FOR_WIN:
                result = True
            else:
                result = False
            output[player] = result
        return output
    
    # Сеттеры
    def add_player_for_game(self, player: Player, bet: int) -> None:
        """ Добавляет игрока в игру с соответствующей ставкой

        Args:
            player (Player): Сам игрок
            bet (int): Его ставка

        Raises:
            ValueError: Вызывается, если на вход подается не экземпляр класса Player
                или ставка не типа данных "int"
            MorePlayersForGame: Задано большое количество игроков (мест больше нет)
            BigBetForPlayer: Ставка слишком большая, у игрока нет столько денег
            RepeatPlayer: Игрок уже с таким именем в игре
            NullMoneyPlayer: У игрока нулевой баланс
        """
        if not isinstance(player, Player):
            raise ValueError('Во входных данных игрок должен быть экземпляром класса "Player"', player)
        if not isinstance(bet, int):
            raise ValueError('Во входных данных ставка должна иметь тип данных "int"', bet)
        if len(self._players) >= Constants.MAX_PLAYERS:
            raise MorePlayersForGame('Задано большое количество игроков. Максимум 6. Вы задали: ', len(self._players)+1)
        else:
            if bet > player.get_count_money():
                raise BigBetForPlayer(f'У игрока {player.name} нет столько денег. Сделайте ставку меньше')
            else:
                if player in self._players:
                    raise RepeatPlayer('Игрок с таким именем в игре уже есть')
                if player.get_count_money() <= 0:
                    raise NullMoneyPlayer('У игрока нет денег для игры')
                self._bets[player] = bet
                self._players.append(player)
    
    # Вспомогательные методы
    
    def clear(self) -> None:
        """ Метод позволяет привести поля в исходное состояние
        """
        # Крупье
        self._dealer = Player('Dealer', Constants.COUNT_MONEY_OF_DEALER)
        # Игроки
        self._players = []
        # Ставки игроков
        self._bets = dict()
        # Индекс текущего игрока
        self._ind_current_player = 0
        # Игральная колода карт
        self._deck = CardDeck()
        
        # Генератор для игры с определенным игроком
        self._gen_for_game = None
    
    def start(self) -> None:
        """ Метод начинает игру
        """
        # Раздаем всем по две карты, а дилеру 1
        for num_card in range(Constants.COUNT_CARDS_WITH_START_GAME_FOR_DEALER):
            self._dealer.add_cards(self._deck.get_card())
        if len(self._players) == 0 or len(self._bets) == 0:
            raise NullCountPlayersForGame('Не добавлены игроки для игры')
        for num_card in range(Constants.COUNT_CARDS_WITH_START_GAME_FOR_ALL_PLAYERS):
            [self._players[ind].add_cards(self._deck.get_card()) for ind in range(len(self._players))]
        # Создаем генератор для игры
        self._gen_for_game = self._generator_for_game()
        next(self._gen_for_game)
    
    def check_stop_game(self) -> tuple[bool, dict[Player, bool] | None]:
        """ Метод проверяет игру на окончание партии. А также возвращает 
            результаты игры.
            Игра считается завершенной, когда дилер набрал 
            "COUNT_POINTS_FOR_STOP_TAKE_CARDS_DIELER"

        Returns:
            tuple[bool, dict[Player, bool]]: 
                [0] - флаг окончание игры
                [1] - Словарь с результатами для каждого игрока,
                    который в качестве ключей содержит объект типа "Player", а
                    данных флаг победы (False - проиграл, True - победил, None - 
                    ничья)   
        """
        output = self._dealer.get_points() >= Constants.COUNT_POINTS_FOR_STOP_TAKE_CARDS_DEALER
        results = None
        # Необходимо распределить ставки, если игра окончена
        if output:
            results = self._scoring()
        return (output, results)
    
    def player_contains_in_game(self, player: Player) -> bool:
        """ Проверяем наличия заданого игрока в игре

        Args:
            player (Player): Игрока, наличие которого необходимо проверить

        Returns:
            bool: false - игрока нет в игре, true - игрок есть в игре
        """
        return player in self._players
    
    def next_player(self) -> None:
        """ После вызова данного метода игра будет происходить со следующим 
            игроком
        """
        if self._ind_current_player <= len(self._players):
            try:
                next(self._gen_for_game)
            except StopIteration:
                pass # Сейчас играет дилер
        else:
            raise AllPlayersPlayed("Все игроки уже сыграли")
    
    def add_card_for_current_player(self) -> None:
        """ Метод добавляет одну карту для текущего игрока
        """
        if self._ind_current_player < len(self._players) and self._players[self._ind_current_player].get_points() < Constants.COUNT_POINTS_FOR_WIN:
            self._players[self._ind_current_player].add_cards(self._deck.get_card())
        elif self._ind_current_player >= len(self._players): 
            if self._dealer.get_points() < Constants.COUNT_POINTS_FOR_WIN:
                # Добавляем карту дилеру (крупье)
                self._dealer.add_cards(self._deck.get_card())
        
        
class MorePlayersForGame(Exception):
    """ Исключение вызывается при попытке игры в большом количестве игроков
    """
    
    def __init__(self, text: str, n: int) -> None:
        self.txt = text
        self.n = n


class AllPlayersPlayed(Exception):
    """ Исключение вызывается при попытке получить следующего игрока, когда
        все уже сыграли
    """
    
    def __init__(self, text: str) -> None:
        self.txt = text
        

class BigBetForPlayer(Exception):
    """ Исключение вызывается при попытке сделать ставку с количеством денег
        выше, чем есть у игрока
    """
    
    def __init__(self, text: str) -> None:
        self.txt = text
        

class RepeatPlayer(Exception):
    """ Исключение вызывается при попытке добавить игроков с одинаковыми именами
    """
    
    def __init__(self, text: str) -> None:
        self.txt = text
      
        
class NullMoneyPlayer(Exception):
    """ Исключение вызывается при попытке добавления игра с нулевым или 
        отрицательным балансом
    """
    
    def __init__(self, text: str) -> None:
        self.txt = text


class NullCountPlayersForGame(Exception):
    """ Исключение вызывается при попытке начать игру с 0 человек
    """
    
    def __init__(self, text: str) -> None:
        self.txt = text
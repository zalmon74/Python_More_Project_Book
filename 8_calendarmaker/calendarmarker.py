""" Модуль содержит основной класс для генерации календаря
"""

from constants import Constants


class CalendarMaker:
    
    def create_title_calendar(self) ->str :
        """ Создаем строку с заголовком для календаря

        Returns:
            str: Строка с заголовком
        """
        output = ''
        for cur_day in Constants.ALL_DAYS_WEEK:
            output += '|' + cur_day + ' '*(Constants.COUNT_COLUMNS_ITEM_CALENDAR-2-len(cur_day))
            if cur_day == Constants.ALL_DAYS_WEEK[-1]:
                output += '|'
        return output   
    
    def _create_item_calendar(self, num_day: int, f_right: bool = True,
                              f_left: bool = True,f_top: bool = True,
                              f_bot: bool = True) -> list[str]:
        """ Метод создания одной ячейки календаря

        Args:
            num_day (int): номер дня, который необходимо установить в ячейке
            f_right (bool): Флаг создания правой стенки. По умочанию True.
            f_left (bool): Флаг создания левой стенки. По умолчанию True.
            f_top (bool): Флаг создания верхней стенки. По умолчанию True.
            f_bot (bool): Флаг создания нижней стенки. По умолчанию True.

        Returns:
            list[str]: Возвращает список со строками, которые содержат
            вывод для консоли (одна строка в списке = одна строка в консоле)
        """
        num_day = str(num_day)
        output = []
        # Создаем первую строку
        if f_top:
            string = '+' if f_left else ''
            string += '-'*(Constants.COUNT_COLUMNS_ITEM_CALENDAR-2)
            string += '+' if f_right else ''
            output.append(string)
        # Создаем боковые стенки
        for num_str in range(Constants.COUNT_STRINGS_ITEM_CALENDAR-2):
            string = '|' if f_left else ''
            if num_str == 0:
                # Добавляем номер дня в ячейку
                for val in num_day:
                    string += val
            else:
                num_day = ''
            string += ' '*(Constants.COUNT_COLUMNS_ITEM_CALENDAR-2-len(num_day))
            string += '|' if f_right else ''
            output.append(string)
        # Создаем последнюю строку
        if f_bot:
            string = '+' if f_left else ''
            string += '-'*(Constants.COUNT_COLUMNS_ITEM_CALENDAR-2)
            string += '+' if f_right else ''
            output.append(string)
        return output

    def _create_N_items_for_calendar(self, lst_days: list[int]) -> list[str]:
        """ Создает N ячеек календаря в одной строке зависимости от размера
            входного списка

        Args:
            lst_days (list[int]): Номера дней, которые должны располагаться ячейки
        
        Returns:
            list[str]: Возвращает список со строками, которые содержат
            вывод для консоли (одна строка в списке = одна строка в консоле)
        """
        count_items = len(lst_days)
        output = []
        for ind in range(count_items):
            if ind == 0:
                lst_item = self._create_item_calendar(lst_days[ind])
                output.extend(lst_item)
            else:
                lst_item = self._create_item_calendar(lst_days[ind],
                                                      f_left=False)
            # Объеденяем ячейки
            if ind != 0:
                for ind_s in range(len(output)):
                    output[ind_s] += lst_item[ind_s]
        return output

    def create_N_M_items_for_calendar(self, mat_days: list[list[int]]) -> list[str]:
        """ Создает NxM ячеек календаря зависимости от размера входной матрица
            с номерами дней

        Args:
            mat_days (list[list[int]]): матрица с намерами дней

        Returns:
            list[str]: Возвращает список со строками, которые содержат
            вывод для консоли (одна строка в списке = одна строка в консоле)
        """
        count_strings = len(mat_days)
        output = []
        # Перебираем по столбцам
        for ind in range(count_strings):
            lst_item = self._create_N_items_for_calendar(mat_days[ind])
            if ind != 0:
                del lst_item[0]
            output.extend(lst_item)
        return output

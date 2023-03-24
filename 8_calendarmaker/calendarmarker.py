""" Модуль содержит основной класс для генерации календаря
"""

from calendar import MONDAY, monthcalendar, monthrange, setfirstweekday

from constants import Constants


class CalendarMaker:
    
    def _create_title_calendar(self) -> str:
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

    def _get_next_prev_max_day_mon(self, year: int, mon: int) -> tuple[int]:
        """ Определяет максимальный день в предыдущем и следующем месяце
            относительно заданного в определенном году

        Args:
            mon (int): Заданный месяц
            year (int): Заданный год

        Returns:
            tuple[int]: Кортеж, который будет содержать два элемента
                [0] - prev_max_day_mon (Количество дней в предыдущем месяце)
                [1] - next_max_day_mon (Количество дней в следующем месяце)
        """
        if mon != 1:
            _, prev_max_day = monthrange(year, mon-1)
        else:
            _, prev_max_day = monthrange(year-1, 12)
        if mon != 12:
            _, next_max_day = monthrange(year, mon+1)
        else:
            _, next_max_day = monthrange(year+1, 1)
        return prev_max_day, next_max_day
    
    def _create_mat_with_days(self, year: int, mon: int) -> list[list[int]]:
        """ создает матрицу с днями для конкртеного месяца и года

        Args:
            year (int): Год
            mon (int): Номер месяца

        Returns:
            list[list[int]]: Созданная матрица с днями
        """
        # Получаем матрицу, но в предыдущем и следующем месяце дни, которые
        # относятся к следующим месяцам заполнены нулями
        output = monthcalendar(year, mon)
        _, curr_max_day_mon = monthrange(year, mon)
        # Определяем количество дней в предыдущем и следующем месяце
        prev_max_day_mon, next_max_day_mon = self._get_next_prev_max_day_mon(year, mon)
        # Заполняем не нулями дни, которые находятся в одной недели 
        # Первый
        index_stop = output[0].index(1)
        day = prev_max_day_mon - index_stop + 1
        for cur_ind in range(index_stop):
            output[0][cur_ind] = day
            day += 1
        # Последний
        index_start = output[-1].index(curr_max_day_mon)+1
        day = 1
        for cur_ind in range(index_start, 7):
            output[-1][cur_ind] = day
            day += 1
        return output

    def _create_N_M_items_for_calendar(self, mat_days: list[list[int]]) -> list[str]:
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

    def _create_name_file(self, year: int, mon: int) -> str:
        """ Создает имя файла для сохранения календаря по умолчанию

        Args:
            year (int): Год
            mon (int): Месяц

        Returns:
            str: Созданное имя файла
        """
        return f'calendar_{year}_{mon}.txt'
    
    def _save_str_to_file(self, string: str, name_file) -> None:
        """ Сохраняет строку в файл

        Args:
            string (str): Строка, которую необходимо сохранить
            name_file (str): Имя файла
        """
        with open(name_file, 'w') as file:
            file.write(string)
    
    def __init__(self) -> None:
        # Устанавливаем, что неделя начинается с понедельника
        setfirstweekday(MONDAY)

    def create_calendar(self, year: int, mon: int) -> str:
        """ Создает календарь на заданный год и месяц в виде строковых
            объектов

        Args:
            year (int): Год
            mon (int): Месяц

        Returns:
            str: Строка, которая содержит в себе созданный календарь
        """
        lst_calendar = []
        lst_calendar.append(self._create_title_calendar())
        mat_days = self._create_mat_with_days(year, mon)
        lst_calendar.extend(self._create_N_M_items_for_calendar(mat_days))
        return '\n'.join(lst_calendar)
    
    def create_calendar_and_save_in_file(self, year: int, mon: int, name_file: str = None) -> None:
        """ Создает календарь и записывает его в файл

        Args:
            year (int): Год
            mon (int): Месяц
            name_file (str): Имя файла, если не задано, то генерируется 
                автоматически. По умолчанию None.
        """
        # Создаем календарь
        calendar_str = self.create_calendar(year, mon)
        # Сохраняем его в файл
        name_file = name_file or self._create_name_file(year, mon)
        self._save_str_to_file(calendar_str, name_file)

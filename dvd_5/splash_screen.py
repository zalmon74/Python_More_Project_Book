""" Основной файл проекта
"""

import random
from time import sleep

import bext
from functions import clear_console


class SplashScreen:
    
    def _get_size_window(self) -> None:
        """ Метод получает размеры окна консоли
        """
        self.width_window, self.height_window = bext.size()
        
    def _get_start_coordinates(self) -> tuple[int]:
        """ Метод генерирует координаты для начала движения слова

        Returns:
            tuple[int]: Кортеж, который имеет два элемента x, y = output
        """
        x = random.randint(0, self.width_window - len(self.printing_figure))
        y = random.randint(0, self.height_window - len(self.printing_figure))
        return x, y
    
    def _get_start_coordinates_for_all_figures(self) -> tuple[list[int]]:
        """ Метод возвращает кортеж с двумя элементами, которые хранят начальные 
            координаты по x и y каждого объекта

        Returns:
            tuple[list[int]]: кортеж с двумя элементами, которые хранят начальные 
            координаты по x и y каждого объекта
        """
        lst_x_coord = []
        lst_y_coord = []
        for _ in range(self.count_figures):
            x, y = self._get_start_coordinates()
            lst_x_coord.append(x)
            lst_y_coord.append(y)
        return lst_x_coord, lst_y_coord
    
    def _get_current_steps(self, lst_x: list[int], lst_y: list[int], lst_step_x: list[int], lst_step_y: list[int], ind_f: int):
        """ Метод определяет значение шагов по координатам для заданной фигуры

        Args:
            lst_x (list[int]): Содержит координаты x для каждой фигуры
            lst_y (list[int]): Содержит координаты y для каждой фигуры
            lst_step_x (list[int]): Содержит значение шага для координаты x 
                для каждой фигуры
            lst_step_y (list[int]): Содержит значение шага для координаты y
                для каждой фигуры
            ind_f (int): Индекс текущей фигуры
        """
        # Определяем необходимо ли изменять координаты и шаги
        if lst_x[ind_f] >= self.width_window - len(self.printing_figure):
            lst_x[ind_f] = self.width_window - len(self.printing_figure)
            lst_step_x[ind_f] = -1
        elif lst_x[ind_f] <= 0:
            lst_x[ind_f] -= lst_step_x[ind_f]
            lst_step_x[ind_f] = 1
        if lst_y[ind_f] >= self.height_window - 1:
            lst_y[ind_f] = self.height_window - 1
            lst_step_y[ind_f] = -1
        elif lst_y[ind_f] <= 0:
            lst_y[ind_f] -= lst_step_y[ind_f]
            lst_step_y[ind_f] = 1
        
    
    def _animation(self) -> None:
        """ Метод, которая отвечает за передвижение фигуры
        """
        lst_x, lst_y = self._get_start_coordinates_for_all_figures()
        lst_step_x = [1 for _ in range(self.count_figures)]
        lst_step_y = [1 for _ in range(self.count_figures)]
        
        while True:
            # определяем размер окна
            self._get_size_window()
            # Очищаем окно
            clear_console()
            # Перебираем все фигуры
            for ind_f in range(self.count_figures):
                # Определяем текущие шаги
                self._get_current_steps(lst_x, lst_y, lst_step_x, lst_step_y, ind_f)
                # Рисуем
                bext.goto(abs(lst_x[ind_f]), abs(lst_y[ind_f]))
                print(self.printing_figure, end='')
                # Шагаем и записываем новые координаты
                lst_x[ind_f] += lst_step_x[ind_f]
                lst_y[ind_f] += lst_step_y[ind_f]
                # Создаем задержку для анимации
                if ind_f == self.count_figures-1:
                    sleep(self.time_sleep)
                
    def __init__(self) -> None:
        self.time_sleep = 0.1
        
        self._get_size_window()
        
        self.set_count_figures()
        self.set_printing_figure()
        self.set_collor_figure()
        
    def set_count_figures(self, count: int = 2) -> None:
        """ Устанавливает количество элементов, которые будут двигаться на экране

        Args:
            count (int): Устанавливаемое количество. По умолчанию 2.
        """
        self.count_figures = count
    
    def set_printing_figure(self, figure: str = 'DVD') -> None:
        """ Устанавливает строку, которая будет перемещаться по экрану

        Args:
            figure (str): Строка, которая будет бегать по экрану. По умолчанию 'DVD'.
        """
        self.printing_figure = figure
    
    def set_collor_figure(self, color: str = 'random') -> None:
        """ Устанавливает цвет объекта, который перемещается по экрау

        Args:
            color (str): Цвет, который необходимо установить. По умолчанию 'random'
        """
        bext.fg(color)
    
    def start(self) -> None:
        """ Метод, который запускает анимацию
        """
        # Вызываем функцию, описывающую анимацию движения
        try:
            self._animation()
        except KeyboardInterrupt:
            clear_console()

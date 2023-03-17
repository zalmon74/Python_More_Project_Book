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
    
    def _is_collision_figures(self, lst_x: list[int], lst_y: list[int], lst_step_x: list[int], lst_step_y: list[int]) -> list[tuple[int]]:
        """ Метод определяем столкновение объектов

        Args:
            lst_x (list[int]): Содержит координаты x для каждой фигуры
            lst_y (list[int]): Содержит координаты y для каждой фигуры
            lst_step_x (list[int]): Содержит значение шага для координаты x 
                для каждой фигуры
            lst_step_y (list[int]): Содержит значение шага для координаты y
                для каждой фигуры

        Returns:
            list[tuple[int]]: Возвращает список, который содержит кортежи с
                2 индексами фигур, которые столкнулись между собой
        """
        output = []
        # Перебираем каждую фигуру и проверяем, что у нее нет соприкосновений
        # с последующей
        for ind_f_1 in range(len(lst_x)):
            for ind_f_2 in range(len(lst_x)):
                
                if ind_f_1 == ind_f_2:
                    continue
                
                # Разница координат
                diff_x = lst_x[ind_f_1] - lst_x[ind_f_2]
                diff_y = lst_y[ind_f_1] - lst_y[ind_f_2]
                
                # Соприкосновение по x
                if 0 <= abs(diff_x) <= len(self.printing_figure)-1:
                    # Соприкосновение по y
                    if 0 < abs(diff_y) <= 1:                      
                        # ind_f_1 сверху (движется вниз-вправо), ind_f_2 снизу
                        if diff_x > 0 and lst_step_y[ind_f_1] > 0 and lst_step_x[ind_f_1] > 0:
                            lst_step_x[ind_f_1] = -1
                            lst_step_y[ind_f_1] = -1
                            lst_step_x[ind_f_2] = 1
                            lst_step_y[ind_f_2] = 1
                        # ind_f_1 сверху (движется вниз), ind_f_2 снизу (движется вверх)
                        elif diff_x > 0 and (lst_step_y[ind_f_1] > 0 or lst_step_y[ind_f_2] < 0):
                            lst_step_x[ind_f_1] = -1
                            lst_step_y[ind_f_1] = -1
                            lst_step_x[ind_f_2] = 1
                            lst_step_y[ind_f_2] = 1
                        # ind_f_1 сверху (движется вниз-влево), ind_f_2 снизу
                        elif diff_x > 0 and lst_step_y[ind_f_1] > 0 and lst_step_x[ind_f_1] < 0:
                            lst_step_x[ind_f_1] = 1
                            lst_step_y[ind_f_1] = -1
                            lst_step_x[ind_f_2] = -1
                            lst_step_y[ind_f_2] = 1
                        # ind_f_1 снизу (движется вверх-вправо), ind_f_2 сверху
                        elif diff_x < 0 and lst_step_y[ind_f_1] < 0 and lst_step_x[ind_f_1] > 0:
                            lst_step_x[ind_f_1] = -1
                            lst_step_y[ind_f_1] = 1
                            lst_step_x[ind_f_2] = 1
                            lst_step_y[ind_f_2] = -1
                        # ind_f_1 снизу (движется вверх), ind_f_2 сверху (движется вниз)
                        elif diff_x > 0 and (lst_step_y[ind_f_1] > 0 or lst_step_y[ind_f_2] < 0):
                            lst_step_x[ind_f_1] = 1
                            lst_step_y[ind_f_1] = 1
                            lst_step_x[ind_f_2] = -1
                            lst_step_y[ind_f_2] = -1
                        # ind_f_1 сверху (движется вниз-влево), ind_f_2 снизу
                        elif diff_x > 0 and lst_step_y[ind_f_1] > 0 and lst_step_x[ind_f_1] < 0:
                            lst_step_x[ind_f_1] = 1
                            lst_step_y[ind_f_1] = 1
                            lst_step_x[ind_f_2] = -1
                            lst_step_y[ind_f_2] = -1
        return output
    
    def _get_current_steps_for_current_figure(self, lst_x: list[int], lst_y: list[int], lst_step_x: list[int], lst_step_y: list[int], ind_f: int):
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
    
    def _get_current_steps(self, lst_x: list[int], lst_y: list[int], lst_step_x: list[int], lst_step_y: list[int], ind_f: int):
        """ Метод определяет значение шагов по координатам

        Args:
            lst_x (list[int]): Содержит координаты x для каждой фигуры
            lst_y (list[int]): Содержит координаты y для каждой фигуры
            lst_step_x (list[int]): Содержит значение шага для координаты x 
                для каждой фигуры
            lst_step_y (list[int]): Содержит значение шага для координаты y
                для каждой фигуры
            ind_f (int): Индекс текущей фигуры
        """
        # Определяем необходимо ли изменять координаты и шаги для выбранной фигры
        self._get_current_steps_for_current_figure(lst_x, lst_y, lst_step_x, lst_step_y, ind_f)
        #
        self._is_collision_figures(lst_x, lst_y, lst_step_x, lst_step_y)
    
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

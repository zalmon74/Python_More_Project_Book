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
        x = random.randint(0, self.width_window - 1)
        y = random.randint(0, self.height_window - 1)
        return x, y
    
    def _get_current_steps(self, x, y, step_x, step_y) -> tuple[int]:
        if x >= self.width_window - len(self.printing_figure):
            x = self.width_window - len(self.printing_figure)
            step_x = -1
        elif x <= 0:
            x -= step_x
            step_x = 1
        if y >= self.height_window - 1:
            y = self.height_window - 1
            step_y = -1
        elif y <= 0:
            y -= step_y
            step_y = 1
        return x, y, step_x, step_y
    
    def _animation(self) -> None:
        x, y = self._get_start_coordinates()
        step_x = step_y = 1
        
        while True:
            # определяем размер окна
            self._get_size_window()
            # Определяем текущие шаги
            x, y, step_x, step_y = self._get_current_steps(x, y, step_x, step_y)
            # Рисуем и очищаем 
            clear_console()
            bext.goto(x, y)
            print(self.printing_figure, end='')
            x += step_x
            y += step_y
            sleep(self.time_sleep)
                
    def __init__(self) -> None:
        self.time_sleep = 0.2
        
        self._get_size_window()
        
        self.set_printing_figure()
        self.set_collor_figure()
        
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
        # Вызываем функцию, описывающую анимацию движения
        try:
            self._animation()
        except KeyboardInterrupt:
            clear_console()

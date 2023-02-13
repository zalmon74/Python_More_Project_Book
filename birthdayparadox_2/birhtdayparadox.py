""" Содержит описание основного класса моделирования
"""


import random

from constants import Constants

class BirthdayParadox:
    """ Класс для моделиварония
    
        Моделирование осуществляется путем формирования множества с днями 
        рождениями для заданного количества человек. Определение совпадения
        осуществляется с помощью разности размера множества и количеством людей
        учавствующих в моделировании. После всех итераций производится
        статистических анализ совпадений.
    """
    
    def _generate_set_with_birthday(self) -> None:
        """ Метод генерирует множество, которое содержит номера дней, когда у 
            людей будет день рождение
        """
        return set(random.randint(0, 364) for _ in range(self.count_people))
    
    def _get_count_people(self) -> int:
        """ Запрос у пользователя количество людей для моделирования

        Returns:
            int: Введенное количество людей
        """
        self.count_people = int(input('Введите количество людей в группе для моделирования: '))
    
    def _start_modeling(self) -> None:
        """ Функция описывает процесс моделирования совпадения дней рождения
        """
        for num_iter in range(Constants.COUNT_ITERATIONS_FOR_MODELING):
            set_birhtday = self._generate_set_with_birthday()
            if self.count_people-len(set_birhtday) >= Constants.COUNT_PEOPLE_WITH_ONE_BIRHTDAY-1:
                self.count_coincidences += 1        
    
    def _calculate_statistic(self) -> float:
        """ Метод рассчитывает статистическую вероятность совпадения дней 
            рождения у людей в одной группе

        Returns:
            float: Статистическая вероятность совпадения дней рождения у людей
            в одной группе
        """
        return round(
            self.count_coincidences/Constants.COUNT_ITERATIONS_FOR_MODELING*100, 
            3
        )
    
    def _print_statistics(self) -> None:
        """ Метод выводит на экран вероятность статистическую вероятность
            совпадения дней рождения у людей в группе
        """
        print(f'Вероятность совпадения дня рождения у {Constants.COUNT_PEOPLE_WITH_ONE_BIRHTDAY} людей в одной группе из {self.count_people} человек составляет: {self._calculate_statistic()}%.')
    
    def __init__(self) -> None:
        # Количество людей в группе (количество моделируемых чисел)
        self.count_people = None
        # Количество совпадений
        self.count_coincidences = 0
    
    def start(self) -> None:
        """ Запуск моделирования
        """
        # Просим пользователя ввести количество людей в группе
        self._get_count_people()
        # Производим моделирование
        self._start_modeling()
        # Выводим полученную статистическую вероятность
        self._print_statistics()
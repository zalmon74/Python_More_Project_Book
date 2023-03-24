import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

    
def input_only_int(text_for_input: str, text_addition: str = '') -> int:
    """ Замена стандартному input, который на выходе дает только значения,
        которые можно преобразовать в int от пользователя

    Args:
        text_for_input (str): текст, который отображается в строчке при вводе
        text_addition (str): Допонительный текст, который необходим 
        пользователю для понимания. По умолчанию пустая строка.

    Returns:
        int: Введенное пользователем значение
    """
    value = None
    while not value and value != 0:
        try:
            clear_console()
            if len(text_addition) > 0:
                print(text_addition)
            value = int(input('\n' + text_for_input))
        except ValueError:
            value = None
    return value


def get_input_year() -> int:
    """ Функция запрашивает у пользователя номер года, для которого необходимо
        создать календарь

    Returns:
        int: Введенный год от пользователя

    """
    output = None
    while not output:
        output = input_only_int('Введите год, для которого хотите создать календарь: ')
    return output


def get_input_monath() -> int:
    """ Функция запрашивает у пользователя номер месяца, для которого необходимо
        создать календарь

    Returns:
        int: Номер месяца, который ввел пользователь
    """
    output = None
    while not output or output > 12:
        output = input_only_int('Введите номер месяца, для которого хотите создать календарь (1-12): ')
    return output


def get_flag_save_in_file() -> bool:
    """ Функция запрашивает у пользователя флаг записи календаря в файл

    Returns:
        bool: Флаг записи в файл
    """
    output = None
    while not output or (output != 1 and output != 2):
        output = input_only_int('Введите 1 - если не хотите записывать календарь в файл, 2 - если хотите записать календарь в файл: ')
    output = False if output == 1 else True
    return output

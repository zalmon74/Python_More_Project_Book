""" Модуль для запуска программы
"""

from calendarmarker import CalendarMaker
from functions import *


def main() -> None:
    year = get_input_year()
    monath = get_input_monath()
    f_save = get_flag_save_in_file()
    calendar = CalendarMaker()
    if f_save:
        calendar.create_calendar_and_save_in_file(year, monath)
    else:
        calendar_str = calendar.create_calendar(year, monath)
        clear_console()
        print(calendar_str)


if __name__ == '__main__':
    main()

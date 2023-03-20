""" Основной файл запуска программы
"""

from cli.cli import CLICaesarCipherHack


def main():
    program = CLICaesarCipherHack()
    program.start()
    
    
if __name__ == '__main__':
    main()

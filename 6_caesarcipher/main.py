""" Основной файл запуска программы
"""

from cli.cli import CLICaesarCipher


def main():
    program = CLICaesarCipher()
    program.start()
    
    
if __name__ == '__main__':
    main()

""" Основной файл проекта для запуска
"""


from cli.cli import CLIBlackJack


def main():
    cli_game = CLIBlackJack()
    cli_game.start()
    
    
if __name__ == '__main__':
    main()


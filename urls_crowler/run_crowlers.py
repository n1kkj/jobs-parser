import click

from crowlers import SberCrowler, YandexCrowler, AvitoCrowler, SberDevCrowler


@click.command()
def run_crowlers():
    print('Sber links:')
    print(*SberCrowler.parse_links(), sep='\n')

    print('Yandex links:')
    print(*YandexCrowler.parse_links(), sep='\n')

    print('Avito links:')
    print(*AvitoCrowler.parse_links(), sep='\n')

    print('SberDev links:')
    print(*SberDevCrowler.parse_links(), sep='\n')


if __name__ == '__main__':
    run_crowlers()

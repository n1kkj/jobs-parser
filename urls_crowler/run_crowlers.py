import click

from crowlers import (
    SberCrowler,
    YandexCrowler,
    AvitoCrowler,
    SberDevCrowler,
    OzonCrowler,
    MtsCrowler,
    DolgoprudnyHhCrowler,
)


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

    print('Ozon links:')
    print(*OzonCrowler.parse_links(), sep='\n')

    print('MTS links:')
    print(*MtsCrowler.parse_links(), sep='\n')

    # print('Dolgoprudny hh links:')
    # print(*DolgoprudnyHhCrowler.parse_links(), sep='\n')


if __name__ == '__main__':
    run_crowlers()

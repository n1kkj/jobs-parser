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
    print('\n1) Sber links:')
    print(*SberCrowler.parse_links(), sep='\n')

    print('\n2) Yandex links:')
    print(*YandexCrowler.parse_links(), sep='\n')

    print('\n3) Avito links:')
    print(*AvitoCrowler.parse_links(), sep='\n')

    print('\n4) SberDev links:')
    print(*SberDevCrowler.parse_links(), sep='\n')

    print('\n5) Ozon links:')
    print(*OzonCrowler.parse_links(), sep='\n')

    print('\n6) MTS links:')
    print(*MtsCrowler.parse_links(), sep='\n')

    print('\n7) Dolgoprudny hh links:')
    print(*DolgoprudnyHhCrowler.parse_links(), sep='\n')


if __name__ == '__main__':
    run_crowlers()

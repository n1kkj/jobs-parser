import click
from datetime import datetime

from crowlers import (
    SberCrowler,
    YandexCrowler,
    AvitoCrowler,
    SberDevCrowler,
    OzonCrowler,
    MtsCrowler,
    DolgoprudnyHhCrowler,
    CareerspaceCrowler,
    ChangellengeCrowler,
    ITFutCrowler,
)

CROWLERS = [
    SberCrowler,
    YandexCrowler,
    AvitoCrowler,
    SberDevCrowler,
    OzonCrowler,
    MtsCrowler,
    DolgoprudnyHhCrowler,
    CareerspaceCrowler,
    ChangellengeCrowler,
    ITFutCrowler,
]


@click.command()
def run_crowlers():
    start_time = datetime.now()

    all_links = []

    for crowler in CROWLERS:
        links = crowler.parse_links()
        all_links.extend(links)
        print(*links, sep='\n')

    end_time = datetime.now() - start_time

    print(len(all_links))
    print(end_time)


if __name__ == '__main__':
    run_crowlers()

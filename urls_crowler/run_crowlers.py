import click
from datetime import datetime, timedelta

from crowlers import (
    SberCrowler,
    YandexCrowler,
    AvitoCrowler,
    SberDevCrowler,
    OzonCrowler,
    MtsCrowler,
    HhCrowler,
    CareerspaceCrowler,
    ChangellengeCrowler,
    ITFutCrowler,
)

CROWLERS = [
    AvitoCrowler,
    SberDevCrowler,
    CareerspaceCrowler,
    ChangellengeCrowler,
    ITFutCrowler,
    SberCrowler,
    YandexCrowler,
    OzonCrowler,
    MtsCrowler,
    HhCrowler,
]


@click.command()
def run_crowlers():

    test_total_times = []
    test_crowlers_time = dict([(i.__str__(), []) for i in CROWLERS])

    for t in range(10):
        print(f'\nStarting test {t}\n')
        print(f'|{"Site":12}|{"Num":8}|{"Time":9}|')
        print(f'|{"-" * 32}')
        start_time = datetime.now()
        all_links = []

        for crowler in CROWLERS:
            crowler_time = datetime.now()
            links = crowler.parse_links()

            crowler_end_time = (datetime.now() - crowler_time)

            all_links.extend(links)

            print(f'|{crowler.__str__():12}|{len(links):8}|{str(crowler_end_time)[2:-3]:9}|')

            test_crowlers_time[crowler.__str__()].append(crowler_end_time)

        end_time = datetime.now() - start_time

        print(f'Total links: {len(all_links)}')
        print(f'Total time: {end_time}')
        test_total_times.append(end_time)

    av_total_time = sum(test_total_times, timedelta(seconds=0)) / len(test_total_times)
    min_time = min(test_total_times)
    max_time = max(test_total_times)

    av_test_crowlers_time = dict(
        [(key, sum(value, timedelta(seconds=0)) / (len(value) + 1)) for key, value in test_crowlers_time.items()]
    )

    print(f'\nav_total_time: {av_total_time}')
    print(f'min_time: {min_time}')
    print(f'max_time: {max_time}')
    print('\nAverage crowlers times:')
    for key, value in av_test_crowlers_time.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    run_crowlers()

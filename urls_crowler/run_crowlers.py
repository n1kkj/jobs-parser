import threading
from datetime import datetime, timedelta

from app.parsers import ParserFactory, SeleniumParserEngine, NoSuchParserError
from app.storages import PandasXLSXStorage
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
    # ChangellengeCrowler,
    ITFutCrowler,
    SberCrowler,
    # YandexCrowler,
    OzonCrowler,
    # MtsCrowler,
    HhCrowler,
]


def run_crowlers_with_pd():
    pandas_xlsx_storage = PandasXLSXStorage(
        "result.xlsx", "unsuccessful_result.xlsx"
    )
    parser_factory = ParserFactory()
    selenium_parser_engine = SeleniumParserEngine()

    all_links = []
    for crowler in CROWLERS:
        all_links.append(crowler.get_links()[0])
        print(f'Finished {crowler.__str__()}')

    for url in all_links:
        try:
            parser = parser_factory.get_parser(
                url, parser_engine=selenium_parser_engine
            )

            page_data = parser.parse(url)

            pandas_xlsx_storage.store_one(page_data)

        except NoSuchParserError:
            pandas_xlsx_storage.store_unsuccessful(url)
            print(f"No parser provided for this url: {url}")

        except Exception as err:
            pandas_xlsx_storage.store_unsuccessful(url)
            print(f"Didn't work for next url: {url}, reason: {err}")

    pandas_xlsx_storage.commit()


def run_test_crowlers_individual():

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
            links = crowler.get_links()

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


def run_test_crowlers_threading():
    threads = []
    start_time = datetime.now()
    all_links = []
    print('Start threading')

    for crowler in CROWLERS:
        thread = threading.Thread(target=lambda: all_links.extend(crowler.run_crowl()))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = datetime.now() - start_time
    print(*all_links, sep='\n')
    print(f'Links count: {len(all_links)}')
    print(f'Total time: {end_time}')
    print(f'Parsers av speed: {len(all_links)/end_time.total_seconds():.3} v/sec')


if __name__ == '__main__':
    run_test_crowlers_threading()

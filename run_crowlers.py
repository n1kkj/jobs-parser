import asyncio
import threading
from datetime import datetime

from urls_crowler.crowlers import (
    SberCrowler,
    YandexCrowler,
    AvitoCrowler,
    SberDevCrowler,
    OzonCrowler,
    HhCrowler,
    CareerspaceCrowler,
    ChangellengeCrowler,
    ITFutCrowler,
)
from redis_cache import RedisCache
from storages.pandas_storage import PandasXLSXStorage

CROWLERS = [
    AvitoCrowler,
    SberDevCrowler,
    CareerspaceCrowler,
    ChangellengeCrowler,
    ITFutCrowler,
    SberCrowler,
    YandexCrowler,
    OzonCrowler,
    HhCrowler,
]


async def run_crowlers_threading():
    threads = []
    start_time = datetime.now()
    all_links = []

    redis_cache = RedisCache()
    await redis_cache.connect()

    pandas_xlsx_storage = PandasXLSXStorage('urls_crowler/result.xlsx')

    print('Начал работу')

    for crowler in CROWLERS:
        thread = threading.Thread(target=lambda: all_links.extend(crowler.run_crowl()))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    pandas_xlsx_storage.store_many(all_links)
    pandas_xlsx_storage.commit()
    end_time = datetime.now() - start_time
    print(f'Всего ссылок: {len(all_links)}')
    print(f'Всего времени: {end_time}')
    print(f'Средняя скорость: {len(all_links)/end_time.total_seconds():.3} вакансий/сек')


if __name__ == '__main__':
    asyncio.run(run_crowlers_threading())

import asyncio
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
    print('Произвожу подготовку')
    start_time = datetime.now()

    redis_cache = RedisCache()
    await redis_cache.connect()

    all_data = []
    all_links = []
    cached_links = []

    pandas_xlsx_storage = PandasXLSXStorage('result.xlsx')

    print('Начал работу')

    async def run_crowler(crowler):
        data, links, cached = await crowler.run_crowl(redis_cache)
        all_data.extend(data)
        all_links.extend(links)
        cached_links.extend(cached)

    tasks = [asyncio.create_task(run_crowler(crowler)) for crowler in CROWLERS]
    await asyncio.gather(*tasks)

    print('Сохраняю в файл')
    pandas_xlsx_storage.store_many(all_data)
    pandas_xlsx_storage.commit()
    end_time = datetime.now() - start_time

    print('Очищаю кэш')
    for link in all_links:
        if link not in cached_links:
            await redis_cache.delete(link)

    print('Закончил обработку ссылок, надеюсь вы обрадуетесь результату, жду вас вновь!\n'
          'Приберёг статистику для вас)\n')
    print(f'Всего ссылок: {len(all_links)}')
    print(f'Ссылок взято из кэша: {len(cached_links)/len(all_links)*100:.2}%')
    print(f'Всего времени: {end_time}')
    print(f'Средняя скорость: {len(all_links)/end_time.total_seconds():.3} вакансий/сек')


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(run_crowlers_threading())


if __name__ == '__main__':
    main()

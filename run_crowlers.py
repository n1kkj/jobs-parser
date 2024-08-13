import asyncio
from datetime import datetime

import settings
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
    redis_cache = RedisCache()
    await redis_cache.connect()

    if settings.DELETE_ALL:
        print('Стираю весь кэш')

        all_redis_links = await redis_cache.get_all_keys()
        for redis_link in all_redis_links:
            await redis_cache.delete(redis_link)

    print('Произвожу подготовку')
    start_time = datetime.now()

    all_data = []
    all_links = []
    cached_links = []

    pandas_xlsx_storage = PandasXLSXStorage(settings.FILE_NAME)

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

    if settings.WITH_DELETE:
        print('Очищаю кэш')
        all_redis_links = await redis_cache.get_all_keys()
        for redis_link in all_redis_links:
            if redis_link not in all_links:
                await redis_cache.delete(redis_link)

    await redis_cache.disconnect()

    end_time = datetime.now() - start_time

    print(
        'Закончил обработку ссылок, надеюсь вы обрадуетесь результату, жду вас вновь!\n'
        'Приберёг статистику для вас)\n'
    )
    print(f'Всего ссылок: {len(all_links)}')
    print(f'Ссылок взято из кэша: {len(cached_links)*100//len(all_links)}%')
    print(f'Всего времени: {end_time}')
    print(f'Средняя скорость: {len(all_links)/end_time.total_seconds()} вакансий/сек')


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(run_crowlers_threading())


def run_parser_for_bot():
    main()


if __name__ == '__main__':
    main()

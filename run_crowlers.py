import threading
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
from urls_crowler.dto import ResultMessageDTO

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


def run_crowlers_threading(chat_id):
    print('Произвожу подготовку')
    redis_cache = RedisCache()

    if settings.DELETE_ALL:
        print('Стираю весь кэш')

        all_redis_links = redis_cache.get_all_keys()
        for redis_link in all_redis_links:
            redis_cache.delete(redis_link)

    start_time = datetime.now()
    pandas_xlsx_storage = PandasXLSXStorage(settings.FILE_NAME)
    all_data = []
    all_links = []
    threads = []
    print('Начал работу')

    for crowler in CROWLERS:
        def target_function():
            data, links = crowler.run_crowl(redis_cache, chat_id)
            all_data.extend(data)
            all_links.extend(links)

        thread = threading.Thread(target=target_function)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print('Сохраняю в файл')
    pandas_xlsx_storage.store_many(all_data)
    pandas_xlsx_storage.commit()

    redis_cache.disconnect()

    end_time = datetime.now() - start_time

    result_message = ResultMessageDTO(
        all_links_count = len(all_data),
        time_spent = str(end_time).split('.')[0],
        av_speed = str(len(all_data)/end_time.total_seconds()).split('.')[0],
    )

    print(
        'Закончил обработку ссылок, надеюсь вы обрадуетесь результату, жду вас вновь!\n'
        'Приберёг статистику для вас)\n'
    )
    print(f'Всего вакансий: {result_message.all_links_count}')
    print(f'Всего времени: {result_message.time_spent}')
    print(f'Скорость: {result_message.av_speed} вакансий/сек')

    return result_message


def main(chat_id):
    result_message = run_crowlers_threading(chat_id)
    return result_message


def run_parser_for_bot(chat_id):
    result_message = main(chat_id)
    return result_message


if __name__ == '__main__':
    main(1334928287)

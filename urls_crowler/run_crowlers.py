import logging
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
    VsetiCrowler,
    # AichCrowler, Some strange 'wized' stuff
    ChoiciCrowler,
    # MtsCrowler,  Breaking if caught that it`s a machine
    RemocateCrowler,
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
    VsetiCrowler,
    RemocateCrowler,
    ChoiciCrowler,
]


def run_crowlers_threading(chat_id: int):
    log = logging.getLogger('crowlers')
    log.setLevel('INFO')
    log.warning('Произвожу подготовку')
    redis_cache = RedisCache()

    if settings.DELETE_ALL:
        log.warning('Стираю весь кэш')

        all_redis_links = redis_cache.get_all_keys()
        for redis_link in all_redis_links:
            if redis_link.startswith('http'):
                redis_cache.delete(redis_link)

    start_time = datetime.now()
    pandas_xlsx_storage = PandasXLSXStorage(settings.FILE_NAME)
    all_data = []
    threads = []
    log.warning('Начал работу')

    for crowler in CROWLERS:

        def target_function():
            data, _ = crowler.run_crowl(redis_cache, chat_id)
            all_data.extend(data)

        thread = threading.Thread(target=target_function)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    log.warning('Сохраняю в файл')
    pandas_xlsx_storage.store_many(all_data)
    pandas_xlsx_storage.commit()

    redis_cache.disconnect()

    end_time = datetime.now() - start_time

    result_message = ResultMessageDTO(
        all_links_count=len(all_data),
        time_spent=str(end_time).split('.')[0],
        av_speed=str(len(all_data) / end_time.total_seconds()).split('.')[0],
    )

    log.warning(
        'Закончил обработку ссылок, надеюсь вы обрадуетесь результату, жду вас вновь!\n'
        'Приберёг статистику для вас)\n'
    )
    log.warning(f'Всего вакансий: {result_message.all_links_count}')
    log.warning(f'Всего времени: {result_message.time_spent}')
    log.warning(f'Скорость: {result_message.av_speed} вакансий/сек')

    return result_message


def main(chat_id):
    result_message = run_crowlers_threading(chat_id)
    return result_message


def run_parser_for_bot(chat_id):
    result_message = main(chat_id)
    return result_message


if __name__ == '__main__':
    main(1334928287)

import asyncio
import logging
import threading
from datetime import datetime

import settings
from storages.google_storage import GoogleStorage
from urls_crowler.crowlers import (
    SberCrowler,
    YandexCrowler,
    AvitoCrowler,
    SberDevCrowler,
    OzonCrowler,
    HhCrowler,
    CareerspaceCrowler,
    # ChangellengeCrowler, # Not working rn
    # ITFutCrowler, # Always changing key
    VsetiCrowler,
    # AichCrowler, # Some strange 'wized' stuff
    ChoiciCrowler,
    # MtsCrowler,  # Breaking if caught that it`s a machine
    RemocateCrowler,
    HabrCrowler,
    SuperJobCrowler,
    KasperskyCrowler,
    TwoGisDEVCrowler,
    TwoGisDEVOPSCrowler,
    TwoGisPROJECTCrowler,
    TwoGisANCrowler,
    TwoGisLEADCrowler,
    GazpromCrowler,
    CrocCrowler,
    AlfaCrowler,
    VKCrowler,
    # TBankCrowler, # Cannot get decoding
    YadroCrowler,
    DomrfCrowler,
    MegafonCrowler,
    RosatomCrowler,
    TGCrowler,
)
from redis_cache import RedisCache
from storages.pandas_storage import PandasXLSXStorage
from urls_crowler.dto import ResultMessageDTO, ParseResultDTO

CROWLERS = [
    AvitoCrowler,
    SberDevCrowler,
    CareerspaceCrowler,
    SberCrowler,
    YandexCrowler,
    OzonCrowler,
    HhCrowler,
    VsetiCrowler,
    RemocateCrowler,
    ChoiciCrowler,
    HabrCrowler,
    SuperJobCrowler,
    KasperskyCrowler,
    TwoGisDEVCrowler,
    TwoGisDEVOPSCrowler,
    TwoGisPROJECTCrowler,
    TwoGisANCrowler,
    TwoGisLEADCrowler,
    GazpromCrowler,
    CrocCrowler,
    AlfaCrowler,
    VKCrowler,
    YadroCrowler,
    DomrfCrowler,
    MegafonCrowler,
    RosatomCrowler,
]

log = logging.getLogger('crowlers')
log.setLevel('INFO')


class CrowlersService:
    @staticmethod
    def main_add_permissions(email: str):
        google_storage = GoogleStorage(settings.GOOGLE_API_KEY)
        google_storage.add_permissions([email])

    @staticmethod
    def save_result(pandas_xlsx_storage, google_storage, all_data):
        pandas_xlsx_storage.store_many(all_data)
        pandas_xlsx_storage.commit()
        new_data_len = google_storage.save_many_vacancies(all_data)
        google_link = google_storage.get_spreadsheet_link()
        return new_data_len, google_link

    @staticmethod
    def get_result_message(start_time, new_data_len, google_link):
        end_time = datetime.now() - start_time

        result_message = ResultMessageDTO(
            all_links_count=new_data_len,
            time_spent=str(end_time).split('.')[0],
            av_speed=str(new_data_len / end_time.total_seconds()).split('.')[0],
            google_link=google_link,
        )

        log.warning(
            'Закончил обработку ссылок, надеюсь вы обрадуетесь результату, жду вас вновь!\n'
            'Приберёг статистику для вас)\n'
        )
        log.warning(f'Всего вакансий: {result_message.all_links_count}')
        log.warning(f'Всего времени: {result_message.time_spent}')
        log.warning(f'Скорость: {result_message.av_speed} вакансий/сек')

        return result_message

    @classmethod
    def run_crowlers_threading(cls, chat_id: int):
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
        google_storage = GoogleStorage(settings.GOOGLE_API_KEY)
        all_data = []
        threads = []
        log.warning('Начал работу')

        for crowler in CROWLERS:

            def target_function():
                data, _ = crowler.run_crowl(redis_cache, chat_id)
                log.warning(f'Закончил обработку {crowler.__name__.replace("Crowler", "")}')
                all_data.extend(data)

            thread = threading.Thread(target=target_function)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        log.warning('Сохраняю в файл и в гугл табличку')
        new_data_len, google_link = cls.save_result(pandas_xlsx_storage, google_storage, all_data)
        redis_cache.disconnect()
        result_message = cls.get_result_message(start_time, new_data_len, google_link)

        return result_message

    @staticmethod
    def run_delete_current(chat_id):
        log = logging.getLogger('crowlers')
        log.setLevel('INFO')
        log.warning('Произвожу подготовку')
        redis_cache = RedisCache()

        all_data = []
        threads = []
        log.warning('Начал работу')

        for crowler in CROWLERS:

            def target_function():
                data, _ = crowler.run_crowl(redis_cache, chat_id)
                log.warning(f'Закончил обработку {crowler.__name__.replace("Crowler", "")}')
                all_data.extend(data)

            thread = threading.Thread(target=target_function)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        log.warning('Стираю найденные ссылки')
        links = [i.link for i in all_data]

        for link in links:
            redis_cache.delete(link)

        redis_cache.disconnect()

    @classmethod
    async def run_tg_crowler(cls, chat_id):
        log.warning('Произвожу подготовку')
        redis_cache = RedisCache()
        start_time = datetime.now()
        pandas_xlsx_storage = PandasXLSXStorage(settings.FILE_NAME)
        google_storage = GoogleStorage(settings.GOOGLE_API_KEY, is_tg=True)

        all_data = []
        log.warning('Начал работу')

        service = TGCrowler(
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            phone_number='79939098119',
            bot_token=settings.CODE_BOT_TOKEN,
        )
        data, _ = await service.run_crowl(redis_cache, chat_id)
        all_data.extend(data)
        log.warning(f'Закончил обработку TG')

        log.warning('Добавляю прошлые ссылки')
        all_redis_links = redis_cache.get_all_keys()
        for redis_link in all_redis_links:
            if redis_link.startswith('https://t.me/'):
                cached_data = redis_cache.get(redis_link)
                parse_result = ParseResultDTO.model_validate_json(cached_data)
                all_data.append(parse_result)

        log.warning('Сохраняю в файл и в гугл табличку')
        new_data_len, google_link = cls.save_result(pandas_xlsx_storage, google_storage, all_data)
        redis_cache.disconnect()
        result_message = cls.get_result_message(start_time, new_data_len, google_link)

        return result_message

    @classmethod
    def run_parser_for_bot(cls, chat_id):
        result_message = cls.run_crowlers_threading(chat_id)
        return result_message

    @classmethod
    def run_delete_current_for_bot(cls, chat_id):
        cls.run_delete_current(chat_id)

    @classmethod
    async def run_tg_for_bot(cls, chat_id):
        return await cls.run_tg_crowler(chat_id)


if __name__ == '__main__':
    # CrowlersService.run_delete_current_for_bot(1334928287)
    # CrowlersService.run_parser_for_bot(1334928287)
    result_message = CrowlersService.run_tg_for_bot(1334928287)
    print(result_message)

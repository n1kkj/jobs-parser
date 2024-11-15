from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import KasperskyParser


class KasperskyCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://api.careers.kaspersky.ru/api/Vacancies/GetVacancies?lang=2&pageSize=300'
    vacancies_prefix = 'https://careers.kaspersky.ru/vacancy/'
    json_vacancies_path = 'items'
    url_key = 'jobReqId'

    link_parser = KasperskyParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links_from_one(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import SberParser
from urls_crowler.utils.get_data_class import GetDataClass


class SberCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://rabota.sber.ru/public/app-candidate-public-api-gateway/api/v1/publications?take=100'
    vacancies_prefix = 'https://rabota.sber.ru/search/'
    data_get_function = GetDataClass.sber_get_json_data
    json_vacancies_path = 'vacancies'
    url_key = 'internalId'
    links_params = {'skip': int, 'take': int}

    link_parser = SberParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links_from_one(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import OzonParser
from urls_crowler.utils.get_data_class import GetDataClass


class OzonCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://job-api.ozon.ru/vacancy?limit=50'
    vacancies_prefix = 'https://job-api.ozon.ru/vacancy/'
    data_get_function = GetDataClass.get_json_data_by_pages
    json_vacancies_path = 'vacancies'
    url_key = 'hhId'
    links_params = {'limit': int, 'page': int, 'level': str}

    extra_kwargs = {'total_pages_path': 'meta/totalPages', 'vacancies_path': 'items', 'vacancy_path': url_key}

    link_parser = OzonParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

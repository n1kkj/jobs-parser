from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import DomrfParser
from urls_crowler.utils.get_data_class import GetDataClass


class DomrfCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://xn--d1aqf.xn--p1ai/career/ajax/vacancies.php?action=search&query=&city=all&intern=&onlyIT=&company=all&department=all&pageSize=10'
    vacancies_prefix = 'https://xn--d1aqf.xn--p1ai/career/vacancy/'
    data_get_function = GetDataClass.get_json_data_by_pages
    json_vacancies_path = 'vacancies'
    links_params = {}
    url_key = 'id'
    extra_kwargs = {
        'vacancies_left_path': 'meta/left',
        'vacancies_path': 'data',
        'vacancy_path': url_key,
        'vacancies_per_page': 10,
        'page_param': 'page',
    }

    link_parser = DomrfParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links_from_one(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

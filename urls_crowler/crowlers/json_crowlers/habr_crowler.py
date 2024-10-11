from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import HabrParser
from urls_crowler.utils.get_data_class import GetDataClass


class HabrCrowler(BaseJSONUrlCrowler):
    main_ulr = ('https://career.habr.com/api/frontend/vacancies?sort=relevance&type=all&currency=RUR'
                '&s[]=2&s[]=3&s[]=4&s[]=6&s[]=41&s[]=42&s[]=43&s[]=97&s[]=32&s[]=34&s[]=176&s[]=125&s[]=44')
    vacancies_prefix = 'https://career.habr.com'
    data_get_function = GetDataClass.get_json_data_by_pages
    json_vacancies_path = 'vacancies'
    links_params = {}
    url_key = 'id'
    extra_kwargs = {'total_pages_path': 'meta/totalPages', 'vacancies_path': 'list', 'vacancy_path': url_key}

    link_parser = HabrParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links_from_one(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

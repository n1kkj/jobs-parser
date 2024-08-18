from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import HhParser
from urls_crowler.utils.get_data_class import GetDataClass


class HhCrowler(BaseJSONUrlCrowler):
    main_ulr = (
        'https://api.hh.ru/vacancies?per_page=100&area=1&professional_role=156&professional_role=160'
        '&professional_role=10&professional_role=150&professional_role=165&professional_role=73'
        '&professional_role=96&professional_role=164&professional_role=104&professional_role=157'
        '&professional_role=107&professional_role=112&professional_role=113&professional_role=148'
        '&professional_role=114&professional_role=116&professional_role=121&professional_role=124'
        '&professional_role=126'
    )
    vacancies_prefix = 'https://hh.ru/vacancy/'
    data_get_function = GetDataClass.get_json_data_by_pages
    json_vacancies_path = 'vacancies'
    url_key = 'id'
    links_params = {'area': str, 'professional_role': list, 'page': int, 'per_page': int}

    extra_kwargs = {'total_pages_path': 'pages', 'vacancies_path': 'items', 'vacancy_path': url_key}

    link_parser = HhParser

    @classmethod
    async def run_crowl(cls, redis_cache, *args, **kwargs):
        results, all_links = await cls.run_parse_all_links_from_one(redis_cache, *args, **kwargs)
        return results, all_links

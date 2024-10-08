from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import YandexParser
from urls_crowler.utils.get_data_class import GetDataClass


class YandexCrowler(BaseJSONUrlCrowler):
    main_ulr = (
        'https://yandex.ru/jobs/api/publications?cities=moscow&page_size=10000&professions=backend-developer'
        '&professions=ml-developer&professions=frontend-developer&professions=tester&professions=dev-ops'
        '&professions=mob-app-developer&professions=mob-app-developer-android&professions=mob-app-developer'
        '-ios&professions=database-developer&professions=system-developer&professions=full-stack-developer'
        '&professions=ml-researcher'
    )
    vacancies_prefix = 'https://yandex.ru/jobs/vacancies/'
    data_get_function = GetDataClass.get_json_data
    json_vacancies_path = 'results'
    url_key = 'publication_slug_url'
    links_params = {'cities': str, 'professions': list}

    link_parser = YandexParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links_from_one(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

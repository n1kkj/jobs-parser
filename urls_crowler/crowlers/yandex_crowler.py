from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.get_data_class import GetSiteData
from urls_crowler.parsers import YandexParser


class YandexCrowler(BaseJSONUrlCrowler):
    main_ulr = ('https://yandex.ru/jobs/api/publications?cities=moscow&page_size=10000&professions=backend-developer'
                '&professions=ml-developer&professions=frontend-developer&professions=tester&professions=dev-ops'
                '&professions=mob-app-developer&professions=mob-app-developer-android&professions=mob-app-developer'
                '-ios&professions=database-developer&professions=system-developer&professions=full-stack-developer'
                '&professions=ml-researcher')
    vacancies_prefix = 'https://yandex.ru/jobs/vacancies/'
    data_get_function = GetSiteData.get_json_data
    json_vacancies_path = 'vacancies'
    url_key = 'publication_slug_url'
    links_params = {'cities': str, 'professions': list}

    link_parser = YandexParser

    @classmethod
    def run_crowl(cls, *args, **kwargs):
        return cls.run_parse_all_links_from_one(*args, **kwargs)

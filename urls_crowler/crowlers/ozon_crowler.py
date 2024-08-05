from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.get_data_class import GetSiteData


class OzonCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://job-api.ozon.ru/vacancy?limit=50'
    vacancies_prefix = 'https://job.ozon.ru/vacancy/'
    data_get_function = GetSiteData.get_json_data_by_pages
    json_vacancies_path = 'vacancies'
    url_key = 'hhId'
    links_params = {'limit': int, 'page': int, 'level': str}

    extra_kwargs = {
        'total_pages_path': 'meta/totalPages',
        'vacancies_path': 'items',
        'vacancy_path': url_key
    }

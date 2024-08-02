from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler


class OzonCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://job-api.ozon.ru/vacancy'
    vacancies_prefix = 'https://job.ozon.ru/vacancy/'
    json_vacancies_path = 'items'
    url_key = 'hhId'
    links_params = {'limit': int, 'page': int, 'level': str}

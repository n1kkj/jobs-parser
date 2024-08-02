from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler


class SberCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://rabota.sber.ru/public/app-candidate-public-api-gateway/api/v1/publications'
    vacancies_prefix = 'https://rabota.sber.ru/search/'
    json_vacancies_path = 'data/vacancies'
    url_key = 'internalId'
    links_params = {'skip': int, 'take': int}

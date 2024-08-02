from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler


class SberDevCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://developers.sber.ru/kak-v-sbere/_next/data/nB6sHLqkq6AkWrYVIU6Zl/vacancies.json'
    vacancies_prefix = 'https://developers.sber.ru/kak-v-sbere/vacancies/'
    json_vacancies_path = 'pageProps/page/MainContent/0/vacancies'
    url_key = 'slug'
    # links_params = {'skip': int, 'take': int}

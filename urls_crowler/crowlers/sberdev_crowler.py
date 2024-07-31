from urls_crowler.crowlers.base_url_crowler import BaseUrlCrowler
from urls_crowler.get_data_functions import get_json_data


class SberDevCrowler(BaseUrlCrowler):
    main_ulr = 'https://developers.sber.ru/kak-v-sbere/_next/data/nB6sHLqkq6AkWrYVIU6Zl/vacancies.json'
    data_get_function = get_json_data
    # links_params = {'skip': int, 'take': int}

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        vacancies_prefix = 'https://developers.sber.ru/kak-v-sbere/vacancies/'
        vacancies_urls = [
            f'{vacancies_prefix}{x["slug"]}' for x in data['pageProps']['page']['MainContent'][0]['vacancies']  # type: ignore
        ]
        return vacancies_urls

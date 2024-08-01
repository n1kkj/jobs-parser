from urls_crowler.crowlers.base_url_crowler import BaseUrlCrowler
from urls_crowler.get_data_class import GetSiteData


class SberDevCrowler(BaseUrlCrowler):
    main_ulr = 'https://developers.sber.ru/kak-v-sbere/_next/data/nB6sHLqkq6AkWrYVIU6Zl/vacancies.json'
    vacancies_prefix = 'https://developers.sber.ru/kak-v-sbere/vacancies/'
    data_get_function = GetSiteData.get_json_data
    # links_params = {'skip': int, 'take': int}

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        vacancies_urls = [
            f'{cls.vacancies_prefix}{x["slug"]}' for x in data['pageProps']['page']['MainContent'][0]['vacancies']  # type: ignore
        ]
        return vacancies_urls

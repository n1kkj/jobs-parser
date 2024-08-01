from urls_crowler.crowlers.base_url_crowler import BaseUrlCrowler
from urls_crowler.get_data_class import GetSiteData


class SberCrowler(BaseUrlCrowler):
    main_ulr = 'https://rabota.sber.ru/public/app-candidate-public-api-gateway/api/v1/publications'
    vacancies_prefix = 'https://rabota.sber.ru/search/'
    data_get_function = GetSiteData.get_json_data
    links_params = {'skip': int, 'take': int}

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        vacancies_urls = [
            f'{cls.vacancies_prefix}{x["internalId"]}' for x in data['data']['vacancies']  # type: ignore
        ]
        return vacancies_urls

from urls_crowler.crowlers.base_url_crowler import BaseUrlCrowler
from urls_crowler.get_data_class import GetSiteData


class OzonCrowler(BaseUrlCrowler):
    main_ulr = 'https://job-api.ozon.ru/vacancy'
    vacancies_prefix = 'https://job.ozon.ru/vacancy/'
    data_get_function = GetSiteData.get_json_data
    links_params = {'limit': int, 'page': int, 'level': str}

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        vacancies_urls = [
            f'{cls.vacancies_prefix}{x["hhId"]}' for x in data['items']  # type: ignore
        ]
        return vacancies_urls

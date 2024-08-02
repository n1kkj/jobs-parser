from bs4 import BeautifulSoup

from urls_crowler.crowlers.base_url_crowler import BaseUrlCrowler
from urls_crowler.get_data_class import GetSiteData


class MtsCrowler(BaseUrlCrowler):
    main_ulr = 'https://job.mts.ru/vacancies'
    vacancies_prefix = 'https://job.mts.ru'
    data_get_function = GetSiteData.mts_get_html_by_selenium_data
    links_params = {'limit': int, 'page': int, 'level': str}

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        soup = BeautifulSoup(data, 'html.parser')
        vacancies_urls = [
            f'{cls.vacancies_prefix}{x["href"]}' for x in soup.find_all('a', class_='job-list-card card-list__card')
        ]
        return vacancies_urls

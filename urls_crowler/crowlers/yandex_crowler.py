from urls_crowler.crowlers.base_url_crowler import BaseUrlCrowler
from urls_crowler.get_data_class import GetSiteData
from bs4 import BeautifulSoup


class YandexCrowler(BaseUrlCrowler):
    main_ulr = 'https://yandex.ru/jobs/vacancies'
    vacancies_prefix = 'https://yandex.ru'
    data_get_function = GetSiteData.get_html_data
    links_params = {'cities': str, 'professions': list}

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        soup = BeautifulSoup(data, 'html.parser')
        vacancies_urls = [
            f'{cls.vacancies_prefix}{x["href"]}' for x in soup.find_all('a', class_='lc-jobs-vacancy-card__link')
        ]
        return vacancies_urls

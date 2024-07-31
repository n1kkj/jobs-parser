from urls_crowler.crowlers.base_url_crowler import BaseUrlCrowler
from urls_crowler.get_data_functions import get_html_data
from bs4 import BeautifulSoup


class AvitoCrowler(BaseUrlCrowler):
    main_ulr = 'https://career.avito.com/vacancies/'
    data_get_function = get_html_data
    links_params = {'cities': str, 'professions': list}

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        vacancies_prefix = 'https://career.avito.com'
        soup = BeautifulSoup(data, 'html.parser')
        vacancies_urls = [
            f'{vacancies_prefix}{x["href"]}' for x in soup.find_all('a', class_='vacancies-section__item-link')
        ]
        return vacancies_urls

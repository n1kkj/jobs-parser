from urls_crowler.crowlers.base_url_crowler import BaseUrlCrowler
from urls_crowler.get_data_class import GetSiteData
from bs4 import BeautifulSoup


class CareerspaceCrowler(BaseUrlCrowler):
    main_ulr = 'https://careerspace.app/jobs?countryId%5B%5D=d57afff6-27c5-4ab6-a9a1-e183727764e1&functions%5B%5D=8'
    vacancies_prefix = 'https://careerspace.app'
    data_get_function = GetSiteData.get_html_data
    links_params = {'countryId': str, 'functions': str}

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        soup = BeautifulSoup(data, 'html.parser')
        vacancies_urls = [
            f'{cls.vacancies_prefix}{x["href"]}' for x in soup.find_all('a', class_='job-card__i')
        ]
        return vacancies_urls

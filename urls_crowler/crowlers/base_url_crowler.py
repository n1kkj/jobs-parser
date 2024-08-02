from bs4 import BeautifulSoup
import dpath.util

from urls_crowler.get_data_class import GetSiteData


class BaseUrlCrowler:
    """
    Base URL crowler class
    """
    main_ulr = None
    data_get_function = None
    vacancies_prefix = None
    links_params = {}

    @classmethod
    def get_data(cls) -> dict | str:
        """
        Uses self.data_get_function function to parse self.main_ulr
        :return: dict or str of api data
        """
        return cls.data_get_function(cls.main_ulr)

    @classmethod
    def parse_links(cls) -> list:
        """
        Custom for every crouler
        :return: List of links to vacancies
        """
        pass


class BaseHTMLUrlCrowler(BaseUrlCrowler):
    data_get_function = GetSiteData.get_html_data
    html_link_class = None

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        soup = BeautifulSoup(data, 'html.parser')
        vacancies_urls = [
            f'{cls.vacancies_prefix}{x["href"]}' for x in soup.find_all('a', class_=cls.html_link_class)
        ]
        return vacancies_urls


class BaseJSONUrlCrowler(BaseUrlCrowler):
    data_get_function = GetSiteData.get_json_data
    json_vacancies_path = None
    url_key = None

    @classmethod
    def parse_links(cls) -> list:
        data = super().get_data()
        vacancies_urls = [
            f'{cls.vacancies_prefix}{x[cls.url_key]}' for x in dpath.util.get(data, cls.json_vacancies_path)
        ]
        return vacancies_urls

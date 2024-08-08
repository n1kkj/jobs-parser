from bs4 import BeautifulSoup
import dpath.util

from urls_crowler.get_data_class import GetSiteData
from urls_crowler.parsers.base_url_parser import BaseUrlParser


class BaseUrlCrowler:
    """
    Base URL crowler class
    """
    main_ulr = None
    data_get_function = None
    vacancies_prefix = None
    links_params = {}
    extra_kwargs = {}

    link_parser = BaseUrlParser

    @classmethod
    def run_crowl(cls, *args, **kwargs):
        """
        Custom for every crowler
        """

    @classmethod
    def get_data(cls, *args, **kwargs) -> dict | str:
        """
        Uses self.data_get_function function to parse self.main_ulr
        :return: dict or str of api data
        """
        kwargs = cls.extra_kwargs if cls.extra_kwargs else {}
        return cls.data_get_function(cls.main_ulr, *args, **kwargs)

    @classmethod
    def get_links(cls, *args, **kwargs) -> list:
        """
        Custom for every crowler
        :return: List of links to vacancies
        """
        pass

    @classmethod
    def run_parse_all_links(cls):
        links = cls.get_links()
        links_data = cls.link_parser.parse_all_links(links)
        return links_data

    @classmethod
    def run_parse_all_links_from_one(cls):
        data = cls.get_data()
        links_data = cls.link_parser.parse_all_links_from_one(data)
        return links_data

    @classmethod
    def __str__(cls):
        return cls.__name__[:cls.__name__.find('Crowler')]


class BaseHTMLUrlCrowler(BaseUrlCrowler):
    data_get_function = GetSiteData.get_html_data
    html_link_class = None

    @classmethod
    def get_links(cls, *args, **kwargs) -> list:
        data = super().get_data(*args, **kwargs)
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
    def run_parse_all_links(cls, *args, **kwargs):
        links = cls.get_links()
        links_data = cls.link_parser.parse_all_links(links)
        return links_data

    @classmethod
    def run_parse_all_links_from_one(cls, *args, **kwargs):
        data = super().get_data(*args, **kwargs)
        links_data = cls.link_parser.parse_all_links_from_one(data)
        return links_data

    @classmethod
    def get_links(cls, *args, **kwargs) -> list:
        data = super().get_data(*args, **kwargs)
        vacancies_urls = [
            f'{cls.vacancies_prefix}{x[cls.url_key]}' for x in dpath.util.get(data, cls.json_vacancies_path)
        ]
        return vacancies_urls

from typing import List
import dpath.util as du
from bs4 import BeautifulSoup

from urls_crowler.dto import ParseResultDTO
from urls_crowler.get_data_class import GetSiteData


class BaseUrlParser:
    """
    Base URL parser class
    """
    title_key = None
    desc_key = None
    skills_key = None
    salary_key = None
    city_key = None
    employer_key = None

    use_soup_desc = False

    data_get_function = None

    extra_kwargs = {}
    result_dto = ParseResultDTO

    @classmethod
    def get_keys(cls) -> dict:
        return {
            'title': cls.title_key,
            'desc': cls.desc_key,
            'skills': cls.skills_key,
            'salary': cls.salary_key,
            'city': cls.city_key,
            'employer': cls.employer_key,
        }

    @staticmethod
    def get_empty_dict() -> dict:
        return {
            'title': '',
            'desc': '',
            'skills': '',
            'salary': '',
            'city': '',
            'employer': ''
        }

    @classmethod
    def parse_all_links(cls, links) -> List[ParseResultDTO]:
        results = []
        for link in links:
            results.append(cls.parse_link(link))
        return results

    @classmethod
    def parse_link(cls, *args, **kwargs) -> ParseResultDTO:
        """
        Custom for every parser
        :return: Dict of data
        """
        pass

    @classmethod
    def get_data(cls, link, *args, **kwargs) -> dict | str:
        """
        Uses self.data_get_function function to parse self.main_ulr
        :return: dict or str of api data
        """
        kwargs = cls.extra_kwargs if cls.extra_kwargs else {}
        return cls.data_get_function(link, *args, **kwargs)

    @classmethod
    def __str__(cls) -> str:
        return cls.__name__[:cls.__name__.find('Parser')]


class BaseJSONUrlParser(BaseUrlParser):
    data_get_function = GetSiteData.get_json_data

    @classmethod
    def parse_link(cls, link, *args, **kwargs) -> ParseResultDTO:
        data = super().get_data(link)
        keys = super().get_keys()
        empty_dict = super().get_empty_dict()
        result_values = {}

        try:
            for key, value in keys.items():
                res_value = ''

                if value is not None:
                    res_value = str(du.get(data, value))

                    if cls.use_soup_desc and key == 'desc':
                        res_value = BeautifulSoup(res_value, 'html.parser').text

                result_values[key] = res_value

        except Exception as e:
            print(f'Error dealing with link {link}, {e}')
            return ParseResultDTO(**empty_dict)

        return ParseResultDTO(**result_values)

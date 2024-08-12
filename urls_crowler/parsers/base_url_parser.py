import json
import re
from typing import List

import dpath.util as du
from bs4 import BeautifulSoup

from urls_crowler.dto import ParseResultDTO, FixedValuesDTO
from urls_crowler.utils import skills_list
from urls_crowler.utils.get_data_class import GetDataClass


class BaseUrlParser:
    """
    Base URL parser class
    """
    title_key = None
    desc_key = None
    salary_key = None
    exp_key = None
    city_key = None
    employer_key = None

    fixed_title = None
    fixed_desc = None
    fixed_salary = None
    fixed_exp = None
    fixed_city = None
    fixed_employer = None

    vacancies_list_key = None
    vacancies_prefix = None
    url_key = None

    use_soup_desc = False

    data_get_function = None

    extra_kwargs = {}
    result_dto = ParseResultDTO

    @classmethod
    def find_skills(cls, text):
        skills_set = set(skills_list)
        pattern = r"\b(" + "|".join(re.escape(skill) for skill in skills_set) + r")\b"
        skills = re.findall(pattern, text, re.IGNORECASE)
        return ', '.join(set(skills))

    @classmethod
    def get_keys(cls) -> dict:
        return {
            'title': cls.title_key,
            'desc': cls.desc_key,
            'salary': cls.salary_key,
            'exp': cls.exp_key,
            'city': cls.city_key,
            'employer': cls.employer_key,
        }

    @classmethod
    def get_fixed(cls) -> dict:
        raw_fixed = {
            'title': cls.fixed_title,
            'desc': cls.fixed_desc,
            'salary': cls.fixed_salary,
            'exp': cls.fixed_exp,
            'city': cls.fixed_city,
            'employer': cls.fixed_employer,
        }
        prepare_fixed = {}
        for key, value in raw_fixed.items():
            if value:
                prepare_fixed[key] = value
        fixed = FixedValuesDTO(**prepare_fixed)
        return fixed.dict(exclude_unset=True)

    @classmethod
    def parse_all_links(cls, links) -> List[ParseResultDTO]:
        keys = cls.get_keys()
        fixed = cls.get_fixed()
        results = []
        for link in links:
            results.append(cls.parse_link(link, keys, fixed))
        return results

    @classmethod
    def parse_all_links_from_one(cls, data) -> List[ParseResultDTO]:
        """
        Custom for every parser
        :return: Dict of data
        """

    @classmethod
    def parse_link(cls, link, keys, fixed, *args, **kwargs) -> ParseResultDTO:
        """
        Custom for every parser
        :return: Dict of data
        """

    @classmethod
    def get_data(cls, link, *args, **kwargs) -> dict | str:
        """
        Uses self.data_get_function function to parse givven link
        :return: dict or str of api data
        """
        kwargs = cls.extra_kwargs
        return cls.data_get_function(link, *args, **kwargs)


class BaseJSONUrlParser(BaseUrlParser):
    data_get_function = GetDataClass.get_json_data

    @classmethod
    def parse_link(cls, link, keys, fixed, *args, **kwargs) -> ParseResultDTO:
        data = super().get_data(link)
        fixed_keys = fixed.keys()
        result_values = {}

        skills = cls.find_skills(json.dumps(data))
        result_values['skills'] = skills

        for key, value in keys.items():
            res_value = ''

            try:
                if key in fixed_keys:
                    res_value = fixed[key]

                elif value is not None:
                    res_value = str(du.get(data, value))

                    if cls.use_soup_desc and key == 'desc':
                        res_value = BeautifulSoup(res_value, 'html.parser').text

                result_values[key] = res_value

            except Exception as e:
                print(f'Ошибка при обработке ссылки {link}{e}')
                result_values[key] = ''

        result_values['link'] = link + '\n'
        return ParseResultDTO(**result_values)

    @classmethod
    def parse_all_links_from_one(cls, data, *args, **kwargs) -> List[ParseResultDTO]:
        keys = super().get_keys()
        result_all_links = []
        fixed = super().get_fixed()
        fixed_keys = fixed.keys()

        try:
            vacancies_list = du.get(data, cls.vacancies_list_key)
        except KeyError:
            print(f'Произошла ошибка с {cls.__str__}, неверный ключ вакансий: {cls.vacancies_list_key}')
            return []

        for vacancy in vacancies_list:
            result_values = {}

            skills = cls.find_skills(json.dumps(vacancy))
            result_values['skills'] = skills

            link = f'{cls.vacancies_prefix}{du.get(vacancy, cls.url_key)}\n'
            result_values['link'] = link

            for key, value in keys.items():
                res_value = ''

                try:
                    if key in fixed_keys:
                        res_value = fixed[key]

                    elif value is not None:
                        res_value = str(du.get(vacancy, value))

                        if cls.use_soup_desc and key == 'desc':
                            res_value = BeautifulSoup(res_value, 'html.parser').text

                    result_values[key] = res_value

                except Exception as e:
                    print(f'Ошибка при обработке ссылки {link}{e}')
                    result_values[key] = ''

            result_all_links.append(ParseResultDTO(**result_values))

        return result_all_links


class BaseHTMLUrlParser(BaseUrlParser):
    data_get_function = GetDataClass.get_html_data

    @classmethod
    def parse_link(cls, link, keys, fixed, *args, **kwargs) -> ParseResultDTO:
        data = super().get_data(link)
        fixed_keys = fixed.keys()
        result_values = {}

        soup = BeautifulSoup(data, 'html.parser')

        skills = cls.find_skills(soup.text)
        result_values['skills'] = skills

        for key, value in keys.items():
            res_value = ''

            try:
                if key in fixed_keys:
                    res_value = fixed[key]

                elif value is not None:
                    res_value = soup
                    for v in value.split('/'):
                        v = v.split('|')
                        index = v[-1] if str(v[-1]).isdigit() else 0
                        res_value = res_value.find_all(v[0], class_=v[1])[index]
                    res_value = res_value.text if res_value else res_value

                result_values[key] = str(res_value).replace('\xa0', ' ')

            except IndexError:
                print(f'Не найден элемент на странице: {link}')
                result_values[key] = ''
            except Exception as e:
                print(f'Не удалось обработать ссылку {link}\n{e}')
                result_values[key] = ''

        result_values['link'] = link + '\n'
        return ParseResultDTO(**result_values)

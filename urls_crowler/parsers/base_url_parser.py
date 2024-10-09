import json
import logging
import re
from typing import List

import dpath.util as du
from bs4 import BeautifulSoup

import settings
from urls_crowler.dto import ParseResultDTO, FixedValuesDTO
from urls_crowler.utils import skills_dict, ExpCases
from urls_crowler.utils.JOBS_TITLES import job_titles
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
    work_format_key = None

    fixed_title = None
    fixed_desc = None
    fixed_salary = None
    fixed_exp = None
    fixed_city = None
    fixed_employer = None
    fixed_work_format = None

    vacancies_list_key = None
    vacancies_prefix = None
    url_key = None

    use_soup_desc = False

    data_get_function = None

    extra_kwargs = {}
    result_dto = ParseResultDTO
    manager_flags = ('опыт работы руководителем',
                     'опыт управления',
                     'опыт управления проектами',
                     'руководили', 'в подчинении',
                     'опыт управления командой')

    tech_flags = ('техническое образование',
                  'высшее техническое образование',
                  'высшее образование')

    @staticmethod
    def find_skills(text):
        skills_set = set(skills_dict.keys())
        pattern = r'\b(' + '|'.join(re.escape(skill.replace('-', ' ')) for skill in skills_set) + r')\b'
        skills = re.findall(pattern, text, re.IGNORECASE)
        skills = [skill.lower() for skill in skills]
        return list(set(skills))

    @staticmethod
    def format_job_title(raw_title: str) -> str:
        for title in job_titles:
            if title in raw_title.lower():
                return title
        return raw_title

    @staticmethod
    def format_salary(raw_salary: str) -> str:
        matches = re.findall(r'\d+', raw_salary)
        if len(matches) == 2:
            return str(int((int(matches[0]) + int(matches[1])) / 2))
        elif matches:
            return matches[0]

        return raw_salary

    @staticmethod
    def format_exp(text, exp):
        # 1) Опыт не нужен
        for i in ('нет опыта', 'опыт не нужен', 'опыт не требуется'):
            if i in text.lower():
                return 0
        # 2) В строке есть чило
        for char in exp:
            if char.isdigit():
                return int(char)
        # 3) Случай с грейдами
        return ExpCases.get_exp(exp)

    @classmethod
    def find_exp(cls, text, prev_exp):
        # Форматируем опыт
        prev_exp = cls.format_exp(text, prev_exp)

        # Если опыт None, то даем ему -1, чтобы при сравнении был ниже
        if not prev_exp:
            prev_exp = -1

        # По дефолту -2, чтобы при сравнении был ниже
        found_exp = -2

        # Ищем строку со словом опыт
        match = re.search(r'\bОпыт\b', text, re.IGNORECASE)

        # Если нашли, то находим цифру в этом предложении
        if match:
            sentence = text[match.start() : text.find('.', match.start())]
            found_exp = re.search(r'\d+', sentence)
            if found_exp:
                found_exp = int(found_exp.group(0))

        # Если найденный опыт больше предыдущего, то возвращаем новый
        if found_exp > prev_exp:
            return str(found_exp)

        # Если найденный опыт меньше и не было предыдущего, то возвращаем Не найден
        if prev_exp == -1:
            return 'Не найден'

        # В любом другом случае просто возвращаем строку
        return str(prev_exp)

    @staticmethod
    def specify_profession(skills):
        direction_counts = {}

        for skill in skills:
            directions = skills_dict[skill.replace(' ', '-')].split(', ')

            for direction in directions:
                if direction not in direction_counts:
                    direction_counts[direction] = 0
                direction_counts[direction] += 1

        if len(direction_counts.values()) > 0:
            max_count = max(direction_counts.values())
            most_frequent_directions = [
                direction for direction, count in direction_counts.items() if count == max_count
            ]
            return most_frequent_directions[0].split('/')
        return '/'.split('/')

    @classmethod
    def get_keys(cls) -> dict:
        return {
            'title': cls.title_key,
            'desc': cls.desc_key,
            'salary': cls.salary_key,
            'exp': cls.exp_key,
            'city': cls.city_key,
            'employer': cls.employer_key,
            'work_format': cls.work_format_key,
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
            'work_format': cls.fixed_work_format,
        }
        prepare_fixed = {}
        for key, value in raw_fixed.items():
            if value:
                prepare_fixed[key] = value
        fixed = FixedValuesDTO(**prepare_fixed)
        return fixed.model_dump(exclude_unset=True)

    @classmethod
    def tech_true(cls, text):
        for flag in cls.tech_flags:
            if flag in text.lower():
                return True
        return False

    @classmethod
    def manager_true(cls, text):
        for flag in cls.manager_flags:
            if flag in text.lower():
                return True
        return False

    @classmethod
    def parse_all_links(cls, all_links, redis_cache, chat_id) -> (List[ParseResultDTO], List):
        keys = cls.get_keys()
        fixed = cls.get_fixed()
        results = []

        for link in all_links:
            cached_data = redis_cache.get(link)
            if not cached_data:
                parse_result = cls.parse_link(link, keys, fixed)
                results.append(parse_result)
                parse_result.users.append(chat_id)
                parse_result.users = list(set(parse_result.users))
                redis_cache.set(link, parse_result.model_dump_json())
            else:
                parse_result = ParseResultDTO.model_validate_json(cached_data)
                if settings.INCLUDE_PREVIOUS >= (chat_id in parse_result.users):
                    results.append(parse_result)
                    parse_result.users.append(chat_id)
                    parse_result.users = list(set(parse_result.users))
                    redis_cache.set(link, parse_result.model_dump_json())

        return results, all_links

    @classmethod
    def parse_all_links_from_one(cls, data, redis_cache, chat_id) -> (List[ParseResultDTO], List):
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
    def _parse_link(cls, vacancy, result_values, keys, fixed_keys, fixed, link) -> dict:
        skills = cls.find_skills(json.dumps(vacancy))
        result_values['skills'] = ', '.join(skills)
        result_values['tech_flag'] = cls.tech_true(json.dumps(vacancy))
        result_values['manager_flag'] = cls.manager_true(json.dumps(vacancy))
        specify_profession = cls.specify_profession(skills)
        result_values['direction'] = specify_profession[0]
        result_values['profession'] = specify_profession[1]

        for key, value in keys.items():
            res_value = ''

            try:
                if key in fixed_keys:
                    res_value = fixed[key]

                elif value is not None:
                    res_value = str(du.get(vacancy, value))

                    if cls.use_soup_desc and key == 'desc':
                        res_value = BeautifulSoup(res_value, 'html.parser').text

                    if key == 'salary':
                        res_value = cls.format_salary(res_value)

                    if key == 'title':
                        res_value = cls.format_job_title(res_value)

                if key == 'exp':
                    res_value = cls.find_exp(json.dumps(vacancy), res_value)

                result_values[key] = res_value

            except Exception:
                result_values[key] = ''

        return result_values

    @classmethod
    def parse_link(cls, link, keys, fixed, *args, **kwargs) -> ParseResultDTO:
        data = super().get_data(link)
        fixed_keys = fixed.keys()
        result_values = {}

        result_values = cls._parse_link(data, result_values, keys, fixed_keys, fixed, link)

        result_values['link'] = link
        return ParseResultDTO(**result_values)

    @classmethod
    def parse_all_links_from_one(cls, data, redis_cache, chat_id, *args, **kwargs) -> (List[ParseResultDTO], List):
        keys = super().get_keys()
        result_all_data = []
        fixed = super().get_fixed()
        fixed_keys = fixed.keys()

        all_links = []

        try:
            vacancies_list = du.get(data, cls.vacancies_list_key)
        except KeyError:
            logging.warning(f'Произошла ошибка с {cls.__name__}, неверный ключ вакансий: {cls.vacancies_list_key}')
            return [], []

        for vacancy in vacancies_list:
            link = f'{cls.vacancies_prefix}{du.get(vacancy, cls.url_key)}'
            all_links.append(link)

            cached_data = redis_cache.get(link)
            if not cached_data:
                result_values = {'link': link}
                result_values = cls._parse_link(vacancy, result_values, keys, fixed_keys, fixed, link)
                parse_result = ParseResultDTO(**result_values)
                result_all_data.append(parse_result)
                parse_result.users.append(chat_id)
                parse_result.users = list(set(parse_result.users))
                redis_cache.set(link, parse_result.model_dump_json())
            else:
                parse_result = ParseResultDTO.model_validate_json(cached_data)
                parse_result.users = [] if not parse_result.users else parse_result.users
                if settings.INCLUDE_PREVIOUS >= (chat_id in parse_result.users):
                    result_all_data.append(parse_result)
                    parse_result.users.append(chat_id)
                    parse_result.users = list(set(parse_result.users))
                    redis_cache.set(link, parse_result.model_dump_json())

        return result_all_data, all_links


class BaseHTMLUrlParser(BaseUrlParser):
    data_get_function = GetDataClass.get_html_data

    @classmethod
    def parse_link(cls, link, keys, fixed, *args, **kwargs) -> ParseResultDTO:
        data = super().get_data(link)
        fixed_keys = fixed.keys()
        result_values = {}

        soup = BeautifulSoup(data, 'html.parser')

        skills = cls.find_skills(soup.text)
        result_values['skills'] = ', '.join(skills)
        result_values['tech_flag'] = cls.tech_true(soup.text)
        result_values['manager_flag'] = cls.manager_true(soup.text)
        specify_profession = cls.specify_profession(skills)
        result_values['direction'] = specify_profession[0]
        result_values['profession'] = specify_profession[1]

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
                    res_value = str(res_value).replace('\xa0', ' ')

                    if key == 'salary':
                        res_value = cls.format_salary(res_value)

                    if key == 'title':
                        res_value = cls.format_job_title(res_value)

                if key == 'exp':
                    res_value = cls.find_exp(soup.text, res_value)

                result_values[key] = res_value

            except IndexError:
                logging.warning(f'Не найден элемент {key}: {value} на странице: {link}')
                result_values[key] = ''
            except Exception:
                result_values[key] = ''

        result_values['link'] = link
        return ParseResultDTO(**result_values)

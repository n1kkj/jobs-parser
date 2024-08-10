from urls_crowler.parsers import BaseJSONUrlParser


class HhParser(BaseJSONUrlParser):
    title_key = 'name'
    desc_key = 'snippet/requirement'
    skills_key = None
    salary_key = None
    city_key = 'area/name'
    employer_key = 'employer/name'

    vacancies_list_key = 'vacancies'
    vacancies_prefix = 'https://hh.ru/vacancy/'
    url_key = 'id'

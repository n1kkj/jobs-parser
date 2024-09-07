from urls_crowler.parsers import BaseJSONUrlParser


class HhParser(BaseJSONUrlParser):
    title_key = 'name'
    desc_key = 'snippet/requirement'
    salary_key = None
    exp_key = 'experience/name'
    city_key = 'area/name'
    employer_key = 'employer/name'
    work_format_key = 'schedule/name'

    vacancies_list_key = 'vacancies'
    vacancies_prefix = 'https://hh.ru/vacancy/'
    url_key = 'id'

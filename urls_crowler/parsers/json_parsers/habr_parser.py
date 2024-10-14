from urls_crowler.parsers import BaseJSONUrlParser


class HabrParser(BaseJSONUrlParser):
    title_key = 'title'
    desc_key = None
    salary_key = 'salary/formatted'
    exp_key = 'salaryQualification'
    city_key = 'locations'
    employer_key = 'company/title'
    work_format_key = 'employment'

    vacancies_list_key = 'vacancies'
    vacancies_prefix = 'https://career.habr.com/vacancies/'
    url_key = 'id'

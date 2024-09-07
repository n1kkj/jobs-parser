from urls_crowler.parsers import BaseJSONUrlParser


class SberParser(BaseJSONUrlParser):
    title_key = 'title'
    desc_key = 'duties'
    salary_key = 'salary_max'
    exp_key = None
    city_key = 'city'
    employer_key = 'company'
    work_format_key = None

    vacancies_list_key = 'vacancies'
    vacancies_prefix = 'https://rabota.sber.ru/search/'
    url_key = 'internalId'

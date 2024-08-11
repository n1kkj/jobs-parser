from urls_crowler.parsers import BaseJSONUrlParser


class SberParser(BaseJSONUrlParser):
    title_key = 'title'
    desc_key = 'duties'
    salary_key = None
    exp_key = 'salary_min'
    city_key = 'city'
    employer_key = 'company'

    vacancies_list_key = 'vacancies'
    vacancies_prefix = 'https://rabota.sber.ru/search/'
    url_key = 'internalId'

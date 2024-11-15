from urls_crowler.parsers import BaseJSONUrlParser


class KasperskyParser(BaseJSONUrlParser):
    title_key = 'titles/title'
    desc_key = None
    salary_key = None
    exp_key = None
    city_key = 'cities'
    employer_key = None
    work_format_key = None

    vacancies_list_key = 'items'
    vacancies_prefix = 'https://careers.kaspersky.ru/vacancy/'
    url_key = 'jobReqId'

    fixed_employer = 'Kaspersky'

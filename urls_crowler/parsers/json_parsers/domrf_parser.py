from urls_crowler.parsers import BaseJSONUrlParser


class DomrfParser(BaseJSONUrlParser):
    title_key = 'name'
    desc_key = 'department'
    salary_key = None
    exp_key = None
    city_key = 'city'
    employer_key = 'company'
    work_format_key = None

    vacancies_list_key = 'vacancies'
    vacancies_prefix = 'https://xn--d1aqf.xn--p1ai/career/vacancy/'
    url_key = 'id'

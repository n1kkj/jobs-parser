from urls_crowler.parsers import BaseJSONUrlParser


class ItFutParser(BaseJSONUrlParser):
    title_key = 'title'
    desc_key = 'description'
    salary_key = None
    exp_key = None
    city_key = None
    employer_key = 'company/alias'

    vacancies_list_key = 'vacancies'
    vacancies_prefix = 'https://it.fut.ru/internship/'
    url_key = 'alias'

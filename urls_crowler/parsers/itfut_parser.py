from urls_crowler.parsers import BaseJSONUrlParser


class ItFutParser(BaseJSONUrlParser):
    title_key = 'title'
    desc_key = 'description'
    skills_key = None
    salary_key = None
    city_key = None
    employer_key = 'company/alias'

    vacancies_list_key = 'vacancies'
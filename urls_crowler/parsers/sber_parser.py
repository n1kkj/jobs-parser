from urls_crowler.parsers import BaseJSONUrlParser


class SberParser(BaseJSONUrlParser):
    title_key = 'name'
    desc_key = 'descr'
    skills_key = 'skills'
    salary_key = None
    city_key = 'city'
    employer_key = 'dep'

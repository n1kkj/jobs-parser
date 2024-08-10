from urls_crowler.parsers import BaseJSONUrlParser


class OzonParser(BaseJSONUrlParser):
    title_key = 'name'
    desc_key = 'descr'
    skills_key = 'skills'
    salary_key = None
    city_key = 'city'
    employer_key = 'dep'

    use_soup_desc = True

from urls_crowler.parsers import BaseJSONUrlParser


class OzonParser(BaseJSONUrlParser):
    title_key = 'name'
    desc_key = 'descr'
    salary_key = None
    exp_key = 'exp'
    city_key = 'city'
    employer_key = 'dep'
    work_format_key = 'employment'

    use_soup_desc = True

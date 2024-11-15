from urls_crowler.parsers import BaseJSONUrlParser


class AlfaParser(BaseJSONUrlParser):
    title_key = 'name'
    desc_key = 'descriptionText'
    salary_key = None
    exp_key = 'experience'
    city_key = 'city'
    employer_key = None
    work_format_key = None

    fixed_employer = 'Альфа'

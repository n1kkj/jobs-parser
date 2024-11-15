from urls_crowler.parsers import BaseHTMLUrlParser


class TwoGisParser(BaseHTMLUrlParser):
    title_key = 'h1|vacancy__title'
    desc_key = 'div|vacancy__text/p|'
    salary_key = None
    exp_key = None
    city_key = None
    employer_key = None
    work_format_key = 'div|tag vacancy__tag tag--relocation tag--tooltip/div|tag__text'

    fixed_employer = '2Гис'

    use_soup_desc = True

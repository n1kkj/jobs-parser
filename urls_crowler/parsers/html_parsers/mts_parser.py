from urls_crowler.parsers import BaseHTMLUrlParser


class MtsParser(BaseHTMLUrlParser):
    title_key = 'h1|col-mob-4 title'
    desc_key = None
    salary_key = None
    exp_key = None
    city_key = None
    employer_key = None
    work_format_key = None

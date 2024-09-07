from urls_crowler.parsers import BaseHTMLUrlParser


class ChoiciParser(BaseHTMLUrlParser):
    title_key = None
    desc_key = None
    salary_key = None
    exp_key = None
    city_key = None
    employer_key = None
    work_format_key = None

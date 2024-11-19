from urls_crowler.parsers import BaseHTMLUrlParser


class YadroParser(BaseHTMLUrlParser):
    title_key = 'h1|h2'
    desc_key = 'div|vpage__content'
    salary_key = None
    exp_key = None
    city_key = None
    employer_key = None
    work_format_key = None

from urls_crowler.parsers import BaseHTMLUrlParser


class AichParser(BaseHTMLUrlParser):
    title_key = 'h1|heading-style-h4'
    desc_key = 'div|text-rich-text_job w-richtext'
    salary_key = None
    exp_key = None
    city_key = None
    employer_key = None
    work_format_key = None

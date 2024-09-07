from urls_crowler.parsers import BaseHTMLUrlParser


class RemocateParser(BaseHTMLUrlParser):
    title_key = 'h1|top-title-job'
    desc_key = 'div|text-rich-text w-richtext'
    salary_key = None
    exp_key = None
    city_key = None
    employer_key = None
    work_format_key = 'div|job-tag'

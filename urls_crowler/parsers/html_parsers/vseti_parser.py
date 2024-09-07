from urls_crowler.parsers import BaseHTMLUrlParser


class VsetiParser(BaseHTMLUrlParser):
    title_key = 'h1|heading-9'
    desc_key = 'div|rich-text-block w-richtext'
    salary_key = 'p|skills1-in-job|-1'
    exp_key = 'p|skills1-in-job'
    city_key = None
    employer_key = 'p|paragraph-23 hfdfdjdf jfdjdf'
    work_format_key = 'p|skills1-in-job|-2'

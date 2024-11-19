from urls_crowler.parsers import BaseHTMLUrlParser


class VKParser(BaseHTMLUrlParser):
    title_key = 'h1|title-main mobile-only'
    desc_key = 'div|article'
    salary_key = None
    exp_key = 'div|vacancy-tag|-2'
    city_key = None
    employer_key = None
    work_format_key = 'div|vacancy-tag'

    fixed_employer = 'VK'

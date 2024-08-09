from urls_crowler.parsers import BaseHTMLUrlParser


class ChangellengeParser(BaseHTMLUrlParser):
    title_key = 'h1|vacancy-without-form-header'
    desc_key = 'div|vacancy-without-form-bottom-block/h2|'
    skills_key = None
    salary_key = 'div|vacancy-without-form-salary'
    city_key = 'h3|vacancy-without-form-tag__city/span|'
    employer_key = None

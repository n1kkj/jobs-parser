from urls_crowler.parsers import BaseHTMLUrlParser


class ChangellengeParser(BaseHTMLUrlParser):
    title_key = 'h1|vacancy-without-form-header'
    desc_key = 'div|vacancy-without-form-bottom-block/h2|'
    salary_key = 'div|vacancy-without-form-salary'
    exp_key = 'h3|vacancy-without-form-tag__experience'
    city_key = 'h3|vacancy-without-form-tag__city/span|'
    employer_key = None
    work_format_key = 'h3|vacancy-without-form-tag__employment'

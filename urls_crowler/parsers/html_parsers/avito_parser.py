from urls_crowler.parsers import BaseHTMLUrlParser


class AvitoParser(BaseHTMLUrlParser):
    title_key = 'div|page-info/h1|'
    desc_key = 'section|vacancies-detail__description'
    salary_key = None
    exp_key = None
    city_key = 'span|page-info__link-text'
    employer_key = None
    work_format_key = 'span|page-info__link-text'

    fixed_employer = 'Avito'

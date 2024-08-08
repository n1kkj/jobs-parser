from urls_crowler.parsers import BaseHTMLUrlParser


class AvitoParser(BaseHTMLUrlParser):
    title_key = 'div|page-info/h1|'
    desc_key = 'section|vacancies-detail__description/p|'
    skills_key = None
    salary_key = None
    city_key = 'span|page-info__link-text'
    employer_key = None

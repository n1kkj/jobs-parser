from urls_crowler.parsers import BaseHTMLUrlParser


class SberDevParser(BaseHTMLUrlParser):
    title_key = 'h1|sc-45e1da05-0 sc-81d0f9f1-7 QPtSW kFPzMP'
    desc_key = 'div|sc-iGgWBj sc-45e1da05-25 sc-26c5ab91-3 faWaSL XArFl iNiqbL'
    salary_key = None
    exp_key = 'div|sc-81d0f9f1-12 jsWPdY|1'
    city_key = 'div|sc-81d0f9f1-12 jsWPdY|0'
    employer_key = 'span|sc-fd3988f5-10 gcZxDC'
    work_format_key = None

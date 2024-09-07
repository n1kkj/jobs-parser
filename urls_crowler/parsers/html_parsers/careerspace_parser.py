from urls_crowler.parsers import BaseHTMLUrlParser


class CareerspaceParser(BaseHTMLUrlParser):
    title_key = 'h1|cs-t cs-t--title32job cs-t--base-text-color cs-t--initial cs-t--700 cs-mb28'
    desc_key = 'div|j-d__dsc-vl'
    salary_key = 'div|price'
    exp_key = None
    city_key = 'span|job-lb__tx'
    employer_key = 'div|j-d-h__bl cs-df-alc-jsb/span|'
    work_format_key = 'span|job-lb__tx|0'

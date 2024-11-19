from urls_crowler.parsers import BaseHTMLUrlParser


class TBankParser(BaseHTMLUrlParser):
    title_key = 'div|amAHGn'
    desc_key = 'div|amAHGn|1'
    salary_key = None
    exp_key = 'div|aZ2btx'
    city_key = 'div|cZ2btx'
    employer_key = None
    work_format_key = None

    fixed_employer = 'T-Bank'
    use_utf_8 = True

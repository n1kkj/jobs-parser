from urls_crowler.parsers import BaseHTMLUrlParser


class RosatomParser(BaseHTMLUrlParser):
    title_key = 'h2|chakra-heading css-16e95kr'
    desc_key = 'p|chakra-text css-1ukmq8g'
    salary_key = 'div|css-2jrvi6'
    exp_key = 'div|css-16dqfiv'
    city_key = 'div|css-1ydqi8z'
    employer_key = None
    work_format_key = 'div|css-1emztro'

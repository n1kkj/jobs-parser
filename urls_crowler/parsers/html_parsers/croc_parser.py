from urls_crowler.parsers import BaseHTMLUrlParser


class CrocParser(BaseHTMLUrlParser):
    title_key = 'h1|mb-smaller mb-md-smallest'
    desc_key = 'div|mb-big mb-md-biggest vacancy-detail__content-main-text-block'
    salary_key = None
    exp_key = 'li|bg-color-light_blue br-80 px-smallest py-tiny size-md-smallest'
    city_key = None
    employer_key = None
    work_format_key = 'li|bg-color-light_blue br-80 px-smallest py-tiny size-md-smallest|1'

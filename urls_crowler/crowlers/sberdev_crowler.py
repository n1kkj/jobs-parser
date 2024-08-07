from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler


class SberDevCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://developers.sber.ru/kak-v-sbere/vacancies?city=moscow'
    vacancies_prefix = 'https://developers.sber.ru/'
    html_link_class = 'sc-14149c6a-1 dZZpyw'
    links_params = {}

from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import SberDevParser
from urls_crowler.utils import GetDataClass


class SberDevCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://developers.sber.ru/kak-v-sbere/vacancies?city=moscow'
    data_get_function = GetDataClass.get_html_data_by_scrolling
    vacancies_prefix = 'https://developers.sber.ru/'
    html_link_class = 'sc-14149c6a-1 dZZpyw'
    links_params = {}

    link_parser = SberDevParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

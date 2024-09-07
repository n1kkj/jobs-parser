from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import ChoiciParser
from urls_crowler.utils import GetDataClass


class ChoiciCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://choicy.work/'
    vacancies_prefix = ''
    html_link_class = 'bubble-element Link baTaNaIi clickable-element'
    data_get_function = GetDataClass.get_html_data_by_scrolling

    link_parser = ChoiciParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

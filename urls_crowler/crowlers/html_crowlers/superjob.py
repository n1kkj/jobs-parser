from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import SuperJobParser
from urls_crowler.utils import GetDataClass


class SuperJobCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://www.superjob.ru/vakansii/programmist.html'
    vacancies_prefix = ''
    data_get_function = GetDataClass.get_html_data_by_scrolling
    html_link_class = 'EWWny'
    links_params = {}

    link_parser = SuperJobParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

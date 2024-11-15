from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import CrocParser
from urls_crowler.utils.get_data_class import GetDataClass


class CrocCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://careers.croc.ru/vacancies/?sections=7%2C19%2C15%2C17%2C13'
    vacancies_prefix = 'https://careers.croc.ru/'
    data_get_function = GetDataClass.get_html_data_by_pages
    html_link_class = 'size-normal size-md-smaller'

    extra_kwargs = {'page_param': 'num=page-'}

    link_parser = CrocParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

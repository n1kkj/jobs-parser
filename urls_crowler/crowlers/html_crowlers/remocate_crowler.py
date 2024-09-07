from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import RemocateParser
from urls_crowler.utils import GetDataClass


class RemocateCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://www.remocate.app/'
    vacancies_prefix = 'https://www.remocate.app'
    html_link_class = 'job-card w-inline-block'
    data_get_function = GetDataClass.get_html_data_by_scrolling

    link_parser = RemocateParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

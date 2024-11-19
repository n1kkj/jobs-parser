from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import MegafonParser
from urls_crowler.utils.get_data_class import GetDataClass


class MegafonCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://job.megafon.ru/vacancy/all/it-reshenia'
    vacancies_prefix = 'https://job.megafon.ru'
    data_get_function = GetDataClass.get_html_data_by_pages
    html_link_class = 'tile__link'

    extra_kwargs = {'page_param': 'page=', 'page_url_prefix': '?'}

    link_parser = MegafonParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

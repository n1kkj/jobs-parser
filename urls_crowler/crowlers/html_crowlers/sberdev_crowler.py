from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import SberDevParser


class SberDevCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://developers.sber.ru/kak-v-sbere/vacancies?city=moscow'
    vacancies_prefix = 'https://developers.sber.ru/'
    html_link_class = 'sc-14149c6a-1 dZZpyw'
    links_params = {}

    link_parser = SberDevParser

    @classmethod
    async def run_crowl(cls, redis_cache, *args, **kwargs):
        results, all_links = await cls.run_parse_all_links(redis_cache, *args, **kwargs)
        return results, all_links

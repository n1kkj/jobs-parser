from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import AvitoParser


class AvitoCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://career.avito.com/vacancies/?q=&action=filter&direction=razrabotka&location%5B%5D=moskva'
    vacancies_prefix = 'https://career.avito.com'
    html_link_class = 'vacancies-section__item-link'
    links_params = {'cities': str, 'professions': list, 'direction': str}

    link_parser = AvitoParser

    @classmethod
    async def run_crowl(cls, redis_cache, *args, **kwargs):
        results, all_links, cached_links = await cls.run_parse_all_links(redis_cache, *args, **kwargs)
        return results, all_links, cached_links

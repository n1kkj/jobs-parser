from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import GazpromParser


class GazpromCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://www.gazprombank.tech/_next/data/8F4wzZeoF4sFF85bzr34t/vacancies.json'
    vacancies_prefix = 'https://www.gazprombank.tech/_next/data/8F4wzZeoF4sFF85bzr34t'
    json_vacancies_path = 'pageProps/json/vacancies'

    url_key = 'url'
    add_after_url_key = '.json'

    link_parser = GazpromParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

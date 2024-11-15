from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import AlfaParser


class AlfaCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://job.alfabank.ru/api/vacancies?city=0100&tag=1043&tag=1284&tag=1191&tag=1386&tag=1015&tag=1216&tag=1142&take=200'
    vacancies_prefix = 'https://job.alfabank.ru/api/vacancies/'
    json_vacancies_path = 'items'

    url_key = 'id'

    link_parser = AlfaParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

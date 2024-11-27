from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import TwoGisParser


class TwoGisBaseCrowler(BaseHTMLUrlCrowler):
    main_ulr = ''
    vacancies_prefix = 'https://job.2gis.ru/'
    html_link_class = 'rubric__name'

    link_parser = TwoGisParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links


class TwoGisDEVCrowler(TwoGisBaseCrowler):
    main_ulr = 'https://job.2gis.ru/software/'


class TwoGisDEVOPSCrowler(TwoGisBaseCrowler):
    main_ulr = 'https://job.2gis.ru/admin/'


class TwoGisPROJECTCrowler(TwoGisBaseCrowler):
    main_ulr = 'https://job.2gis.ru/project/'


class TwoGisANCrowler(TwoGisBaseCrowler):
    main_ulr = 'https://job.2gis.ru/analytics/'


class TwoGisLEADCrowler(TwoGisBaseCrowler):
    main_ulr = 'https://job.2gis.ru/team-management/'

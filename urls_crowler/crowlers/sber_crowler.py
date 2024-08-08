from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.get_data_class import GetSiteData
from urls_crowler.parsers import SberParser


class SberCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://rabota.sber.ru/public/app-candidate-public-api-gateway/api/v1/publications?take=100'
    vacancies_prefix = 'https://rabota.sber.ru/search/'
    data_get_function = GetSiteData.sber_get_json_data
    json_vacancies_path = 'vacancies'
    url_key = 'internalId'
    links_params = {'skip': int, 'take': int}

    link_parser = SberParser

    @classmethod
    def run_crowl(cls):
        return cls.run_parse_all_links_from_one()

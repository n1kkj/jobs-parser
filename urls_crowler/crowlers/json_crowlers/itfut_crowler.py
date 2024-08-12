from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
from urls_crowler.parsers import ItFutParser
from urls_crowler.utils.get_data_class import GetDataClass


class ITFutCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://it.fut.ru/_next/data/rlVDKpJCpjJDJkIK7FQrD/internship.json?alias_company_or_type=internship'
    vacancies_prefix = 'https://it.fut.ru/internship/'
    data_get_function = GetDataClass.itfut_get_json_data
    json_vacancies_path = 'pageProps/data/publications'
    url_key = 'alias'
    links_params = {}

    extra_kwargs = {
        'json_vacancies_path': json_vacancies_path
    }

    link_parser = ItFutParser

    @classmethod
    def run_crowl(cls):
        return cls.run_parse_all_links_from_one()

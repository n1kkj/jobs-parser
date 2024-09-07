from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import AichParser
from urls_crowler.utils import GetDataClass


class AichCrowler(BaseHTMLUrlCrowler):
    main_ulr = ('https://h.careers/jobs?professions=%D0%9C%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%BC%D0%B5%D0%BD%D1%82+'
                '%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D0%B0%2C%D0%9C%D0%B5%D0%BD%D0%B5%D0%B4%D0%B6%D0%BC%D0%'
                'B5%D0%BD%D1%82+%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BE%D0%B2%2C%D0%A0%D0%B0%D0%B7%D1%80%D0%B0%'
                'D0%B1%D0%BE%D1%82%D0%BA%D0%B0%2C%D0%90%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%D0%B0')
    vacancies_prefix = ''
    data_get_function = GetDataClass.get_html_data_by_scrolling
    html_link_class = 'n_job_item w-inline-block'
    links_params = {}

    link_parser = AichParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

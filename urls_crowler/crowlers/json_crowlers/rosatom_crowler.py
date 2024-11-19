from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import RosatomParser
from urls_crowler.utils import GetDataClass


class RosatomCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://rosatom-career.ru/vacancies'
    vacancies_prefix = 'https://rosatom-career.ru/'
    data_get_function = GetDataClass.get_html_data_by_clicking
    html_link_class = 'css-1lk1lgh'

    extra_kwargs = {'button_xpath': '//*[@id="__next"]/main/section/div[4]/div/div[2]/ul/li[9]'}

    link_parser = RosatomParser


    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

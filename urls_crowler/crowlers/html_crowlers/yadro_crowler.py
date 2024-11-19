from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import YadroParser
from urls_crowler.utils import GetDataClass


class YadroCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://careers.yadro.com/'
    vacancies_prefix = ''
    data_get_function = GetDataClass.get_html_data_by_clicking
    html_link_class = 'vac__result-item-title'

    extra_kwargs = {'button_xpath': '//*[@id="vfilter__container"]/div/div[2]/div[2]/div/button'}

    link_parser = YadroParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

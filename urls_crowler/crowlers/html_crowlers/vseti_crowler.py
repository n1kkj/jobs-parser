from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import VsetiParser
from urls_crowler.utils.get_data_class import GetDataClass


class VsetiCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://www.vseti.app/jobs'
    vacancies_prefix = ''
    data_get_function = GetDataClass.get_html_data_by_clicking
    html_link_class = 'card-jobs jfdjdf w-inline-block'
    links_params = {'limit': int, 'page': int, 'level': str}
    extra_kwargs = {'button_xpath': '/html/body/div[9]/div/div[1]/div[3]/a[2]/div'}

    link_parser = VsetiParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

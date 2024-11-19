from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import VKParser
from urls_crowler.utils import GetDataClass


class VKCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://team.vk.company/vacancy/?search=&town='
    vacancies_prefix = 'https://team.vk.company'
    data_get_function = GetDataClass.get_html_data_by_clicking
    html_link_class = 'vacancy_vacancyItem__jrNqL'

    extra_kwargs = {'button_xpath': '//*[@id="__next"]/main/section[2]/div/button[1]'}

    link_parser = VKParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

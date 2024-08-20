from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import ChangellengeParser
from urls_crowler.utils.get_data_class import GetDataClass


class ChangellengeCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://changellenge.com/vacancy/filter/stazhirovka-v-it/'
    data_get_function = GetDataClass.get_html_data_by_scrolling
    vacancies_prefix = 'https://changellenge.com'
    html_link_class = 'new-vacancies-card__link new-vacancies-card__logo-wrapper'
    links_params = {}

    link_parser = ChangellengeParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

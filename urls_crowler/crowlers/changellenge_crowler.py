from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.get_data_class import GetSiteData
from urls_crowler.parsers import ChangellengeParser


class ChangellengeCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://changellenge.com/vacancy/filter/indystry-is-it/apply/index.php'
    data_get_function = GetSiteData.get_html_data_by_scrolling
    vacancies_prefix = 'https://changellenge.com'
    html_link_class = 'new-vacancies-card__link new-vacancies-card__logo-wrapper'
    links_params = {}

    link_parser = ChangellengeParser

    @classmethod
    def run_crowl(cls, *args, **kwargs):
        return cls.run_parse_all_links(*args, **kwargs)

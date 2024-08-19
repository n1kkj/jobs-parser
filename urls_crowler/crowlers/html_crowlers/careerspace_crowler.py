from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import CareerspaceParser


class CareerspaceCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://careerspace.app/jobs?countryId%5B%5D=d57afff6-27c5-4ab6-a9a1-e183727764e1&functions%5B%5D=8'
    vacancies_prefix = 'https://careerspace.app'
    html_link_class = 'job-card__i'
    links_params = {'countryId': str, 'functions': str}

    link_parser = CareerspaceParser

    @classmethod
    def run_crowl(cls, redis_cache, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, *args, **kwargs)
        return results, all_links

from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.get_data_class import GetSiteData


class ChangellengeCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://changellenge.com/vacancy/filter/indystry-is-it/apply/index.php'
    data_get_function = GetSiteData.get_html_data_by_scrolling
    vacancies_prefix = 'https://changellenge.com'
    html_link_class = 'new-vacancies-card__link new-vacancies-card__logo-wrapper'
    links_params = {}

from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler


class ChangellengeCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://changellenge.com/vacancy/filter/indystry-is-it/apply/index.php'
    vacancies_prefix = 'https://changellenge.com'
    links_params = {}
    html_link_class = 'new-vacancies-card__link new-vacancies-card__logo-wrapper'

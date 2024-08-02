from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler


class AvitoCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://career.avito.com/vacancies/'
    vacancies_prefix = 'https://career.avito.com'
    html_link_class = 'vacancies-section__item-link'
    links_params = {'cities': str, 'professions': list}

from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.get_data_class import GetSiteData


class MtsCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://job.mts.ru/vacancies'
    vacancies_prefix = 'https://job.mts.ru'
    data_get_function = GetSiteData.mts_get_html_by_selenium_data
    links_params = {'limit': int, 'page': int, 'level': str}
    html_link_class = 'job-list-card card-list__card'

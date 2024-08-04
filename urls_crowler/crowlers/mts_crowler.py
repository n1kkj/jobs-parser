from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.get_data_class import GetSiteData


class MtsCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://job.mts.ru/vacancies'
    vacancies_prefix = 'https://job.mts.ru'
    data_get_function = GetSiteData.get_html_data_by_clicking
    html_link_class = 'job-list-card card-list__card'
    links_params = {'limit': int, 'page': int, 'level': str}
    extra_kwargs = {'button_xpath': '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div/div[4]/button'}

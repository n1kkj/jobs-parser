from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler


class YandexCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://yandex.ru/jobs/vacancies'
    vacancies_prefix = 'https://yandex.ru'
    html_link_class = 'lc-jobs-vacancy-card__link'
    links_params = {'cities': str, 'professions': list}

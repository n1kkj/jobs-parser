from urls_crowler.parsers import BaseJSONUrlParser


class YandexParser(BaseJSONUrlParser):
    title_key = 'title'
    desc_key = 'short_summary'
    salary_key = None
    exp_key = None
    city_key = 'vacancy/cities'
    employer_key = 'public_service/name'
    work_format_key = 'work_modes/'

    vacancies_list_key = 'results'
    vacancies_prefix = 'https://yandex.ru/jobs/vacancies/'
    url_key = 'publication_slug_url'

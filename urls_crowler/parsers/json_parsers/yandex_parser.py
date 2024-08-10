from urls_crowler.parsers import BaseJSONUrlParser


class YandexParser(BaseJSONUrlParser):
    title_key = 'vacancy/profession/name'
    desc_key = 'short_summary'
    skills_key = 'vacancy/skills'
    salary_key = None
    city_key = 'vacancy/cities'
    employer_key = 'public_service/name'

    vacancies_list_key = 'results'
    vacancies_prefix = 'https://yandex.ru/jobs/vacancies/'
    url_key = 'publication_slug_url'

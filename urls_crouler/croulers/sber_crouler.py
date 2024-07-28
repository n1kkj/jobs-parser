from urls_crouler.croulers import BaseUrlCrouler
from urls_crouler.get_data_functions import get_json_data


class SberCrouler(BaseUrlCrouler):
    main_ulr = 'https://rabota.sber.ru/public/app-candidate-public-api-gateway/api/v1/publications'
    data_get_function = get_json_data
    links_params = {'skip': int, 'take': int}

    @classmethod
    def parse_links(cls) -> list:
        data = super(SberCrouler).get_data()
        vacancies_prefix = 'https://rabota.sber.ru/search/'
        vacancies_urls = [f'{vacancies_prefix}{x["internalId"]}' for x in data['data']['vacancies']]  # type: ignore
        return vacancies_urls

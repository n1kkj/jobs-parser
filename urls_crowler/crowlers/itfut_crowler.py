from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler
import dpath.util


class ITFutCrowler(BaseJSONUrlCrowler):
    main_ulr = 'https://it.fut.ru/_next/data/rlVDKpJCpjJDJkIK7FQrD/internship.json?alias_company_or_type=internship'
    vacancies_prefix = 'https://it.fut.ru/internship/'
    json_vacancies_path = 'pageProps/data/publications'
    url_key = 'alias'
    links_params = {}

    @classmethod
    def get_links(cls) -> list:
        data = super().get_data()
        vacancies_urls = []
        try:
            data = [publication for y in dpath.util.get(data, cls.json_vacancies_path) for publication in y]
            vacancies_urls = [
                    f"{cls.vacancies_prefix}{x['company']['alias']}/{x[cls.url_key]}" for x in data
            ]
        except Exception:
            return vacancies_urls
        return vacancies_urls

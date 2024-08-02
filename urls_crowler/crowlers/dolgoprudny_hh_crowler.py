from urls_crowler.crowlers.base_url_crowler import BaseJSONUrlCrowler


class DolgoprudnyHhCrowler(BaseJSONUrlCrowler):
    main_ulr = ('https://api.hh.ru/vacancies?area=2085&search_field=name&search_field=company_name&search_field'
                '=description&enable_snippets=true&L_save_area=true&professional_role=156&professional_role=160'
                '&professional_role=10&professional_role=12&professional_role=150&professional_role=25'
                '&professional_role=165&professional_role=34&professional_role=36&professional_role=73'
                '&professional_role=155&professional_role=96&professional_role=164&professional_role=104'
                '&professional_role=157&professional_role=107&professional_role=112&professional_role=113'
                '&professional_role=148&professional_role=114&professional_role=116&professional_role=121'
                '&professional_role=124&professional_role=125&professional_role=126')
    vacancies_prefix = 'https://hh.ru/vacancy/'
    json_vacancies_path = 'items'
    url_key = 'id'
    links_params = {'area': str, 'professional_role': list, 'page': int, 'per_page': int}

from urls_crowler.parsers import BaseJSONUrlParser


class GazpromParser(BaseJSONUrlParser):
    title_key = 'pageProps/json/title'
    desc_key = 'pageProps/json/description'
    salary_key = None
    exp_key = None
    city_key = 'pageProps/json/place'
    employer_key = 'pageProps/json/team'
    work_format_key = None

    use_soup_desc = True

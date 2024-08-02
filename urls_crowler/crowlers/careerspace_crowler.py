from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler


class CareerspaceCrowler(BaseHTMLUrlCrowler):
    main_ulr = 'https://careerspace.app/jobs?countryId%5B%5D=d57afff6-27c5-4ab6-a9a1-e183727764e1&functions%5B%5D=8'
    vacancies_prefix = 'https://careerspace.app'
    links_params = {'countryId': str, 'functions': str}
    html_link_class = 'job-card__i'

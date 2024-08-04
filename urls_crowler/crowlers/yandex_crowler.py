from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.get_data_class import GetSiteData


class YandexCrowler(BaseHTMLUrlCrowler):
    main_ulr = ('https://yandex.ru/jobs/vacancies?cities=moscow&cities=saint-petersburg&cities=ekaterinburg&cities'
                '=novosibirsk&cities=nizhniy-novgorod&cities=kazan&cities=rostov-on-don&cities=voronezh&cities'
                '=krasnodar&cities=sochi&cities=vladivostok&cities=volgograd&cities=ivanovo&cities=ivanteevka&cities'
                '=izhevsk&cities=innopolis&cities=kaliningrad&cities=lipetsk&cities=omsk&cities=samara&cities=sasovo'
                '&cities=tolyatti&cities=tula&cities=chelyabinsk&professions=backend-developer&professions=ml'
                '-developer&professions=frontend-developer&professions=tester&professions=dev-ops&professions=mob-app'
                '-developer&professions=mob-app-developer-android&professions=mob-app-developer-ios&professions'
                '=database-developer&professions=system-developer&professions=full-stack-developer&professions=ml'
                '-researcher&professions=information-security')
    vacancies_prefix = 'https://yandex.ru'
    data_get_function = GetSiteData.get_html_data_by_scrolling
    html_link_class = 'lc-jobs-vacancy-card__link'
    links_params = {'cities': str, 'professions': list}

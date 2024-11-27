from urls_crowler.crowlers.base_url_crowler import BaseHTMLUrlCrowler
from urls_crowler.parsers import TBankParser
from urls_crowler.utils import GetDataClass


class TBankCrowler(BaseHTMLUrlCrowler):
    main_ulr = (
        'https://www.tbank.ru/career/vacancies/it/?specialty=infrastruktura-administrirovanie&specialty=back'
        '-end-razrabotka&specialty=front-end-razrabotka&specialty=ml&specialty=analitika&specialty=biznes'
        '-analiz&specialty=product-analytics&specialty=system-analysis&specialty=soprovozhdenie-podderzhka'
        '&specialty=product-management&specialty=upravlenie-proektami&grade=junior&grade=middle'
    )
    vacancies_prefix = 'https://www.tbank.ru'
    add_after_url_key = '/'
    data_get_function = GetDataClass.tbank_get_html_data_by_clicking
    html_link_class = 'Button--module__button_a3KMI0 Button--module__button_theme_secondary_j3KMI0'

    extra_kwargs = {
        'button_xpath_start': '/html/body/div[1]/div/div[3]/div/div/div/div[1]/div/div[',
        'button_xpath_end': '1]/button',
    }

    link_parser = TBankParser

    @classmethod
    def run_crowl(cls, redis_cache, chat_id, *args, **kwargs):
        results, all_links = cls.run_parse_all_links(redis_cache, chat_id, *args, **kwargs)
        return results, all_links

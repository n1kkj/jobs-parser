import logging
import time

import dpath.util
import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class GetDataClass:
    @staticmethod
    def get_json_data(url, *args, **kwargs):
        try:
            response = requests.get(url)
            response.raise_for_status()

            if 'application/json' in response.headers['Content-Type']:
                return response.json()
            else:
                raise Exception(f"Ответ не является JSON: {response.headers['Content-Type']}")

        except Exception as e:
            if 'ozon' in url:
                logging.info(f'Скорее всего вакансия скрыта, поэтому у меня не получилось её обработать: {url}')
            logging.error(f'Ошибка при запросе: {e}')
            return {}

    @staticmethod
    def get_chrome_driver():
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--start-maximized')
        # service = Service(executable_path='/usr/bin/chromedriver')
        # driver = webdriver.Chrome(service=service, options=options)
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    @staticmethod
    def get_html_data(url, *args, **kwargs):
        try:
            response = requests.get(url)
            response.raise_for_status()

            if 'text/html' in response.headers['Content-Type']:
                return response.text
            else:
                raise Exception(f"Ответ не является HTML: {response.headers['Content-Type']}")

        except Exception as e:
            logging.error(f'Ошибка при запросе: {e}')
            return ''

    @classmethod
    def get_html_data_by_clicking(cls, url, *args, **kwargs):
        finished = False
        count = 1
        while not finished:
            if count > 100:
                break
            count += 1
            try:
                driver = cls.get_chrome_driver()
                driver.get(url)
                button_xpath = kwargs['button_xpath']

                WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                button = driver.find_element(By.XPATH, button_xpath)

                while button.is_displayed():
                    try:
                        driver.execute_script('arguments[0].click();', button)
                        button = driver.find_element(By.XPATH, button_xpath)
                        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
                    except Exception:
                        break

                time.sleep(1)
                html_content = driver.page_source

                driver.quit()
                finished = True
                return html_content
            except Exception:
                continue

    @classmethod
    def get_html_data_by_scrolling(cls, url, *args, **kwargs):
        try:
            driver = cls.get_chrome_driver()
            driver.get(url)

            last_height = driver.execute_script('return document.body.scrollHeight')

            while True:
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(1.5)
                WebDriverWait(driver, timeout=20).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                new_height = driver.execute_script('return document.body.scrollHeight')
                time.sleep(1.5)
                if new_height == last_height:
                    break

                last_height = new_height

            time.sleep(1)
            html_content = driver.page_source

            driver.quit()

            return html_content

        except Exception as e:
            logging.error(f'Ошибка при запросе: {e}')
            return ''

    @staticmethod
    def get_html_data_by_pages(url, *args, **kwargs):
        html_content = ''

        page_param = kwargs['page_param']

        for page in range(1, 10):
            try:
                response = requests.get(f'{url}&{page_param}{page}')
                response.raise_for_status()

                html_content += response.text
            except Exception:
                continue

        return html_content

    @staticmethod
    def get_json_data_by_pages(url, *args, **kwargs):
        vacancies = []
        data = {}

        total_pages_path = kwargs['total_pages_path']
        vacancies_path = kwargs['vacancies_path']
        vacancy_path = kwargs['vacancy_path']

        response = requests.get(url)
        total_pages = dpath.util.get(response.json(), total_pages_path)

        for page in range(total_pages):
            response = requests.get(f'{url}&page={page}')

            _next_vacancies = response.json()[vacancies_path]
            next_vacancies = []
            for item in _next_vacancies:
                if vacancy_path in item:
                    next_vacancies.append(item)

            vacancies.extend(next_vacancies)

        data['vacancies'] = vacancies
        return data

    @staticmethod
    def sber_get_json_data(url, *args, **kwargs):
        try:
            vacancies = []
            data = {}

            response = requests.get(url)
            response.raise_for_status()
            total_pages = response.json()['data']['total']

            for skip in range(0, total_pages, 100):
                response = requests.get(f'{url}&skip={skip}')
                vacancies.extend(response.json()['data']['vacancies'])

            data['vacancies'] = vacancies
            return data
        except Exception as e:
            logging.error(f'Ошибка при запросе: {e}')
            return ''

    @staticmethod
    def itfut_get_json_data(url, *args, **kwargs):
        try:
            response = requests.get(url)
            response.raise_for_status()

            if 'application/json' in response.headers['Content-Type']:
                data = response.json()
            else:
                logging.error(f"Ответ не является JSON: {response.headers['Content-Type']}")
                data = {}

        except Exception as e:
            logging.error(f'Ошибка при запросе: {e}')
            data = {}

        vacancies = []
        json_vacancies_path = kwargs['json_vacancies_path']
        try:
            vacancies = [publication for y in dpath.util.get(data, json_vacancies_path) for publication in y]
        except KeyError:
            logging.warning(f'Произошла ошибка с {url}, неверный ключ вакансий: {json_vacancies_path}')
        return {'vacancies': vacancies}

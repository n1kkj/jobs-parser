import time

import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GetSiteData:
    @staticmethod
    def get_json_data(url, *args, **kwargs):
        try:
            response = requests.get(url)
            response.raise_for_status()

            if 'application/json' in response.headers['Content-Type']:
                return response.json()
            else:
                raise Exception(f"Ответ не является JSON: {response.headers['Content-Type']}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    @staticmethod
    def get_html_data(url, *args, **kwargs):
        try:
            response = requests.get(url)
            response.raise_for_status()

            if 'text/html' in response.headers['Content-Type']:
                return response.text
            else:
                raise Exception(f"Ответ не является HTML: {response.headers['Content-Type']}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    @staticmethod
    def get_html_data_by_clicking(url, *args, **kwargs):
        try:
            options = ChromeOptions()
            options.add_experimental_option(
                "prefs",
                {
                    "profile.managed_default_content_settings.images": 2,
                },
            )

            driver = webdriver.Chrome(options=options)
            driver.get(url)

            button_xpath = kwargs['button_xpath']

            WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
                (By.XPATH, button_xpath)))
            button = driver.find_element(By.XPATH, button_xpath)

            while button.is_displayed():
                driver.execute_script("arguments[0].click();", button)

                try:
                    button = driver.find_element(By.XPATH, button_xpath)
                except Exception:
                    break

                WebDriverWait(driver, 2).until(EC.element_to_be_clickable(
                    (By.XPATH, button_xpath)))

            time.sleep(1)
            html_content = driver.page_source

            driver.quit()

            return html_content

        except Exception as e:
            raise Exception(f"Ошибка при запросе: {e}")

    @staticmethod
    def get_html_data_by_scrolling(url, *args, **kwargs):
        try:
            options = ChromeOptions()
            options.add_experimental_option(
                "prefs",
                {
                    "profile.managed_default_content_settings.images": 2,
                },
            )

            driver = webdriver.Chrome(options=options)
            driver.get(url)

            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(0.5)
                WebDriverWait(driver, timeout=20).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break

                last_height = new_height

            time.sleep(1)
            html_content = driver.page_source

            driver.quit()

            return html_content

        except Exception as e:
            raise Exception(f"Ошибка при запросе: {e}")

    @staticmethod
    def ozon_get_json_data(url, *args, **kwargs):
        vacancies = []
        data = {}

        response = requests.get(url)
        total_pages = response.json()['meta']['totalPages']

        for page in range(total_pages-1):
            response = requests.get(f'{url}&page={page+1}')
            vacancies.extend(response.json()['items'])

        data['vacancies'] = vacancies
        return data

    @staticmethod
    def sber_get_json_data(url, *args, **kwargs):
        vacancies = []
        data = {}

        response = requests.get(url)
        total_pages = response.json()['data']['total']

        for skip in range(0, total_pages, 100):
            response = requests.get(f'{url}&skip={skip}')
            vacancies.extend(response.json()['data']['vacancies'])

        data['vacancies'] = vacancies
        return data

import time

import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GetSiteData:
    @staticmethod
    def get_json_data(url):
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
    def get_html_data(url):
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
    def mts_get_html_by_selenium_data(url):
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

            button_xpath = '//*[@id="app"]/div[1]/div[3]/div/div/div[2]/div/div[4]/button'

            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, button_xpath)))
            button = driver.find_element(By.XPATH, button_xpath)

            while button.is_displayed():
                driver.execute_script("arguments[0].click();", button)

                try:
                    button = driver.find_element(By.XPATH, button_xpath)
                except Exception as e:
                    break

                WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                    (By.XPATH, button_xpath)))

            time.sleep(1)
            html_content = driver.page_source

            driver.quit()

            return html_content

        except Exception as e:
            raise Exception(f"Ошибка при запросе: {e}")

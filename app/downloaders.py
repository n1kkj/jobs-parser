import csv

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


class YandexLinksDownloader:
    def __init__(self, url: str):
        self.__driver = Chrome()
        self.__url = url

    def download(self):
        links_and_names = self.__get_links_and_names(self.__url)
        self.__save_as_csv(links_and_names)

    def __get_links_and_names(self, url) -> list[tuple[str, str]]:
        self.__driver.get(url)
        elements = self.__driver.find_elements(By.CSS_SELECTOR, "li")

        return list(
            map(
                lambda x: (
                    x.find_element(By.CSS_SELECTOR, "a").get_dom_attribute(
                        "href"
                    ),
                    x.find_element(By.CSS_SELECTOR, "a")
                    .find_element(By.CSS_SELECTOR, "div.text")
                    .find_element(By.CSS_SELECTOR, "p.title")
                    .text,
                ),
                elements,
            )
        )

    def __save_as_csv(self, links: list[tuple[str, str]]):
        with open("links.csv", "w", encoding="utf-8") as file:
            csvwriter = csv.writer(file)

            csvwriter.writerow(["url", "name"])

            for link in links:
                csvwriter.writerow([link[0], link[1]])

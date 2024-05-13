import logging

from downloaders import YandexLinksDownloader

URL = "https://browser.yandex.ru/tab-groupings-share/5fd5ec7b-56cd-4cd4-bdcf-bc44535fb1f5"
# "https://browser.yandex.ru/tab-groupings-share/0c455cac-be2c-48c7-8a5f-c1323e49f808"

if __name__ == "__main__":

    logger = logging.Logger("DOWNLOAD", level=logging.INFO)

    downloader = YandexLinksDownloader(URL)

    downloader.download()

    logger.info("Downloading process successfully finished")

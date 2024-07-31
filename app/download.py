import click
from downloaders import YandexLinksDownloader

# URL = "https://browser.yandex.ru/tab-groupings-share/5fd5ec7b-56cd-4cd4-bdcf-bc44535fb1f5"
# # "https://browser.yandex.ru/tab-groupings-share/0c455cac-be2c-48c7-8a5f-c1323e49f808"


@click.command()
@click.option("--url", help="URL to download from")
def download(url: str) -> None:
    if not url:
        click.echo("You must provide '--url' argument")
        return

    downloader = YandexLinksDownloader(url)

    click.echo("Downloading started...")

    downloader.download()

    click.echo("Downloading finished successfully")


if __name__ == "__main__":
    download()

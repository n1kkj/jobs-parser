import logging

from parsers import NoSuchParserError, ParserFactory, SeleniumParserEngine
from storages import CSVStorage, PandasXLSXStorage

if __name__ == "__main__":
    pandas_xlsx_storage = PandasXLSXStorage(
        "result.xlsx", "unsuccessful_result.xlsx"
    )

    csv_storage = CSVStorage(
        "links.csv", "result.csv", "unsuccessful_result.csv"
    )

    urls = csv_storage.load_urls()

    parser_factory = ParserFactory()

    result = []

    unsuccessful_urls = []

    selenium_parser_engine = SeleniumParserEngine()

    success_counter = 0
    unsuccess_counter = 0

    for url in urls:
        is_already_processed = (
            pandas_xlsx_storage.is_already_parsed_successfully(url)
            or pandas_xlsx_storage.is_already_parsed_unsuccessfully(url)
        )

        if is_already_processed:
            logging.info(f"Next url has already been parsed: {url}")
            continue

        try:
            parser = parser_factory.get_parser(
                url, parser_engine=selenium_parser_engine
            )

            page_data = parser.parse(url)

            pandas_xlsx_storage.store_one(page_data)

            success_counter += 1

        except NoSuchParserError:
            pandas_xlsx_storage.store_unsuccessful(url)
            logging.warning(f"No parser provided for this url: {url}")
            unsuccess_counter += 1

        except Exception as err:
            pandas_xlsx_storage.store_unsuccessful(url)
            logging.warning(f"Didn't work for next url: {url}, reason: {err}")
            unsuccess_counter += 1

        finally:
            print(success_counter, unsuccess_counter)

    pandas_xlsx_storage.commit()

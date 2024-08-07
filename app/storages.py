import csv
import logging

import pandas
from .dto import PageData


def extract_dataframe(page_data: PageData) -> pandas.DataFrame:
    dataframe = pandas.DataFrame(
        [
            [
                page_data.url,
                page_data.vacancy_name,
                page_data.vacancy_description,
                page_data.vacancy_source,
            ]
        ],
        columns=["url", "name", "description", "source"],
    )

    return dataframe


class PandasXLSXUnsuccessfulStorage:
    DATA_COLUMNS = ["url"]

    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name
        self.__file_data = self.__initialize_file()

    def __initialize_file(self) -> pandas.DataFrame:
        try:
            file_data = pandas.read_excel(self.__file_name, index_col=0)

            return file_data

        except FileNotFoundError:
            dataframe = pandas.DataFrame(columns=self.DATA_COLUMNS)
            dataframe.to_excel(self.__file_name)
            return dataframe

    def store_one(self, url: str) -> None:
        self.__file_data = pandas.concat(
            [
                self.__file_data,
                pandas.DataFrame([[url]], columns=self.DATA_COLUMNS),
            ],
            ignore_index=True,
        )

    def commit(self) -> None:
        self.__file_data.to_excel(self.__file_name)

    def __contains__(self, url: str) -> bool:
        assert isinstance(url, str)

        return (self.__file_data == url).any().any()


class PandasXLSXSuccessfulStorage:
    DATA_COLUMNS = ["url", "name", "description", "source"]

    def __init__(self, file_name: str) -> None:
        self.__file_name = file_name

        self.__file_data = self.__initialize_file()

    def __initialize_file(self):
        try:
            file_data = pandas.read_excel(self.__file_name, index_col=0)

            return file_data

        except FileNotFoundError:
            dataframe = pandas.DataFrame(
                columns=self.DATA_COLUMNS,
            )

            dataframe.to_excel(self.__file_name)

            return dataframe

    def store_one(self, page_data: PageData) -> None:
        self.__file_data = pandas.concat(
            [self.__file_data, extract_dataframe(page_data)], ignore_index=True
        )

    def commit(self) -> None:
        self.__file_data.to_excel(
            self.__file_name,
        )

    def __contains__(self, url: str):
        assert isinstance(url, str)

        return (self.__file_data == url).any().any()


class PandasXLSXStorage:
    def __init__(
        self,
        successful_file_name: str,
        unsuccessful_file_name: str,
    ):

        self.__successful_file_name = successful_file_name
        self.__unsuccessful_file_name = unsuccessful_file_name

        self.__unsuccessful_storage = PandasXLSXUnsuccessfulStorage(
            self.__unsuccessful_file_name
        )
        self.__successful_storage = PandasXLSXSuccessfulStorage(
            self.__successful_file_name
        )

    def store_many(self, pages_data: list[PageData]):
        for page_data in pages_data:
            self.__successful_storage.store_one(page_data)

    def store_one(self, page_data: PageData):
        self.__successful_storage.store_one(page_data)

    def commit(self):
        self.__successful_storage.commit()
        self.__unsuccessful_storage.commit()

    def store_unsuccessful(self, url: str):
        self.__unsuccessful_storage.store_one(url)

    def is_already_parsed_successfully(self, url: str) -> bool:
        is_parsed = url in self.__successful_storage

        return is_parsed

    def is_already_parsed_unsuccessfully(self, url: str) -> bool:
        is_parsed = url in self.__unsuccessful_storage

        return is_parsed


class CSVStorage:
    def __init__(
        self,
        from_file_name: str,
        to_file_name: str,
        unsuccessful_to_file_name: str,
    ):
        self.__from_file_name = from_file_name
        self.__to_file_name = to_file_name
        self.__unsuccessful_to_file_name = unsuccessful_to_file_name

    def store(self, pages_data: list[PageData]):
        with open(self.__to_file_name, "w", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(["href", "name", "description", "source"])

            for page_data in pages_data:
                writer.writerow(
                    [
                        page_data.url,
                        page_data.vacancy_name,
                        page_data.vacancy_description,
                        page_data.vacancy_source,
                    ]
                )

    def load_urls(self) -> list[str]:
        with open(self.__from_file_name, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            result = []

            for row in reader:
                if row == []:
                    continue

                if row == ["href", "name"]:
                    continue

                result.append(row[0])

            return result

import pandas

from urls_crowler.dto import ParseResultDTO
from urls_crowler.storages import extract_dataframe


class PandasXLSXStorage:
    DATA_COLUMNS = ['title', 'desc', 'skills', 'salary', 'city', 'employer', 'link']

    def __init__(self, file_name: str):
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

    def store_many(self, pages_data: list[ParseResultDTO]):
        for page_data in pages_data:
            self.store_one(page_data)

    def store_one(self, page_data: ParseResultDTO) -> None:
        self.__file_data = pandas.concat(
            [self.__file_data, extract_dataframe(page_data)], ignore_index=True
        )

    def commit(self) -> None:
        self.__file_data.to_excel(
            self.__file_name,
        )

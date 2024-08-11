import pandas

from urls_crowler.dto import ParseResultDTO
from urls_crowler.storages import extract_dataframe


class PandasXLSXStorage:
    DATA_COLUMNS = ['Компания', 'Должность', 'Требуемый опыт', 'Стек', 'ЗП', 'Описание', 'Город', 'Ссылка']

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__file_data = self.__initialize_file()

    def __initialize_file(self):
        dataframe = pandas.DataFrame(columns=self.DATA_COLUMNS)
        dataframe.to_excel(self.__file_name, index=False)
        return dataframe

    def store_many(self, pages_data: list[ParseResultDTO]):
        for page_data in pages_data:
            self.store_one(page_data)

    def store_one(self, page_data: ParseResultDTO):
        self.__file_data = pandas.concat(
            [self.__file_data, extract_dataframe(page_data)], ignore_index=True
        )

    def commit(self):
        self.__file_data.to_excel(
            self.__file_name,
        )

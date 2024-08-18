import pandas

from urls_crowler.dto import ParseResultDTO
from storages import extract_dataframe


class PandasXLSXStorage:
    DATA_COLUMNS = [
        'Компания',
        'Должность',
        'Направление',
        'Поднаправление',
        'Требуемый опыт',
        'Стек',
        'ЗП',
        'Описание',
        'Город',
        'Ссылка',
    ]

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__file_data = self.__initialize_file()

    def __initialize_file(self):
        dataframe = pandas.DataFrame(columns=self.DATA_COLUMNS)
        dataframe.to_excel(self.__file_name, index=False)

        writer = pandas.ExcelWriter(self.__file_name, engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name='Sheet1', index=False)

        worksheet = writer.sheets['Sheet1']

        for i, col in enumerate(self.DATA_COLUMNS):
            max_len = max(len(str(col)), dataframe[col].astype(str).map(len).max())
            worksheet.set_column(i, i, max_len + 2)

        worksheet.freeze_panes(1, 0)
        writer.save()
        return dataframe

    def store_many(self, pages_data: list[ParseResultDTO]):
        for page_data in pages_data:
            self.store_one(page_data)

    def store_one(self, page_data: ParseResultDTO):
        self.__file_data = pandas.concat([self.__file_data, extract_dataframe(page_data)], ignore_index=True)

    def commit(self):
        self.__file_data.to_excel(
            self.__file_name,
        )

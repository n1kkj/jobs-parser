import pandas as pd

from storages.fields_compare import FieldCompare
from urls_crowler.dto import ParseResultDTO


class PandasXLSXStorage:
    def __init__(self, file_name: str, is_tg: bool=False):
        self.__file_name = file_name
        self.__file_data = self.__initialize_file()
        self.is_tg = is_tg

    @classmethod
    def _get_columns(cls, sheet_name: str, is_tg):
        if is_tg:
            return FieldCompare.columns_tg
        if sheet_name == 'Разработка':
            return FieldCompare.columns_dev
        elif sheet_name == 'Аналитика':
            return FieldCompare.columns_an
        elif sheet_name == 'ML':
            return FieldCompare.columns_ml
        elif sheet_name == 'Product Project':
            return FieldCompare.columns_pr
        else:
            return FieldCompare.columns_dev

    @classmethod
    def extract_dataframe(cls, columns: list, page_data: ParseResultDTO):
        data = []
        for column in columns:
            data.append(FieldCompare.field_compare(column, page_data))
        dataframe = pd.DataFrame([data], columns=columns)
        return dataframe

    def __initialize_file(self):
        sheets = {
            'Разработка': pd.DataFrame(columns=FieldCompare.columns_dev),
            'Аналитика': pd.DataFrame(columns=FieldCompare.columns_an),
            'ML': pd.DataFrame(columns=FieldCompare.columns_ml),
            'Product Project': pd.DataFrame(columns=FieldCompare.columns_pr),
        }
        if self.is_tg:
            sheets = {
                'Разработка': pd.DataFrame(columns=FieldCompare.columns_tg),
                'Аналитика': pd.DataFrame(columns=FieldCompare.columns_tg),
                'ML': pd.DataFrame(columns=FieldCompare.columns_tg),
                'Product Project': pd.DataFrame(columns=FieldCompare.columns_tg),
            }

        with pd.ExcelWriter(self.__file_name, engine='xlsxwriter') as writer:
            for sheet_name, dataframe in sheets.items():
                dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
                worksheet = writer.sheets[sheet_name]

                for i, col in enumerate(self._get_columns(sheet_name, self.is_tg)):
                    worksheet.set_column(i, i, len(col) + 2)

                worksheet.freeze_panes = 'K1'

        return sheets

    def store_many(self, pages_data: list[ParseResultDTO]):
        for page_data in pages_data:
            if page_data.profession is None or page_data.profession == '':
                continue
            sheet_name = self._get_sheet_name(page_data)
            self.__file_data[sheet_name] = pd.concat(
                [self.__file_data[sheet_name], self.extract_dataframe(self._get_columns(sheet_name, self.is_tg), page_data)],
                ignore_index=True,
            )

    def commit(self):
        with pd.ExcelWriter(self.__file_name, engine='xlsxwriter', mode='w') as writer:
            for sheet_name, dataframe in self.__file_data.items():
                dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

    @staticmethod
    def _get_sheet_name(page_data: ParseResultDTO):
        if page_data.direction == 'Разработка':
            return 'Разработка'
        elif page_data.direction == 'Аналитика':
            return 'Аналитика'
        elif page_data.direction == 'ML':
            return 'ML'
        elif page_data.direction == 'Product Project':
            return 'Product Project'
        else:
            return 'Разработка'

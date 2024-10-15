import pandas as pd

from urls_crowler.dto import ParseResultDTO


class PandasXLSXStorage:
    DATA_COLUMNS = [
        'Компания',
        'Должность',
        'Направление',
        'Поднаправление',
        'Требуемый опыт',
        'Стек',
        'ЗП',
        'Техническое образование',
        'Опыт управления',
        'Диапазон ЗП',
        'Описание',
        'Формат работы',
        'Город',
        'Ссылка',
    ]

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__file_data = self.__initialize_file()

    @classmethod
    def extract_dataframe(cls, page_data: ParseResultDTO):
        dataframe = pd.DataFrame(
            [
                [
                    page_data.employer,
                    page_data.title,
                    page_data.direction,
                    page_data.profession,
                    page_data.exp,
                    page_data.skills,
                    page_data.salary,
                    page_data.tech_flag,
                    page_data.manager_flag,
                    page_data.salary_range,
                    page_data.desc,
                    page_data.work_format,
                    page_data.city,
                    page_data.link,
                ]
            ],
            columns=cls.DATA_COLUMNS,
        )

        return dataframe

    def __initialize_file(self):
        sheets = {
            'Разработка': pd.DataFrame(columns=self.DATA_COLUMNS),
            'Аналитика': pd.DataFrame(columns=self.DATA_COLUMNS),
            'ML': pd.DataFrame(columns=self.DATA_COLUMNS),
            'Product Project': pd.DataFrame(columns=self.DATA_COLUMNS),
        }

        with pd.ExcelWriter(self.__file_name, engine='xlsxwriter') as writer:
            for sheet_name, dataframe in sheets.items():
                dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
                worksheet = writer.sheets[sheet_name]

                for i, col in enumerate(self.DATA_COLUMNS):
                    worksheet.set_column(i, i, len(col) + 2)

                worksheet.freeze_panes = 'K1'

        return sheets

    def store_many(self, pages_data: list[ParseResultDTO]):
        for page_data in pages_data:
            if page_data.profession is None or page_data.profession == '':
                continue
            sheet_name = self._get_sheet_name(page_data)
            self.__file_data[sheet_name] = pd.concat(
                [self.__file_data[sheet_name], self.extract_dataframe(page_data)], ignore_index=True
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
        elif page_data.direction in ('Product Management', 'Project  Management'):
            return 'Product Project'
        else:
            return 'Разработка'

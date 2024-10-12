import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

import settings
from urls_crowler.dto import ParseResultDTO


class GoogleStorage:
    columns = [
        'Компания',
        'Должность',
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
    sheets = ['Разработка', 'Аналитика', 'ML', 'Product Project']
    permissions = [
        'nikita.lakin.topka@gmail.com',
        'looandr02@gmail.com',
        'Kuzminiliy@gmail.com',
        '4ingiz.abdrazakov@list.ru',
        'cabdrazakov007@gmail.com',
        'c.abdrazakov@youroffer.ru',
    ]

    def __init__(self, api_file):
        self.sheet_service = None

        self.credentials = None
        self.httpAuth = None
        self.service = None
        self.spreadsheet_id = None

        self.auth(api_file)
        self.set_spreadsheet()
        self.add_permissions()
        self.create_column_names()

    def get_spreadsheet_link(self):
        return f'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}'

    def auth(self, api_file):
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            api_file,
            ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'],
        )
        self.httpAuth = self.credentials.authorize(httplib2.Http())
        self.sheet_service = apiclient.discovery.build('sheets', 'v4', http=self.httpAuth)

    def set_spreadsheet(self):
        _sheets = []
        for i, v in enumerate(self.sheets):
            _sheets.append(
                {
                    'properties': {
                        'sheetType': 'GRID',
                        'sheetId': i,
                        'title': v,
                    }
                }
            )
        spreadsheet = (
            self.sheet_service.spreadsheets()
            .create(
                body={
                    'properties': {'title': 'Parser results', 'locale': 'ru_RU'},
                    'sheets': _sheets,
                }
            )
            .execute()
        )
        self.spreadsheet_id = spreadsheet['spreadsheetId']

    def add_permissions(self):
        self.service = apiclient.discovery.build('drive', 'v3', http=self.httpAuth)
        for i in self.permissions:
            self.service.permissions().create(
                fileId=self.spreadsheet_id,
                body={'type': 'user', 'role': 'writer', 'emailAddress': i},
                fields='id',
            ).execute()

    def create_column_names(self):
        for i in self.sheets:
            self.sheet_service.spreadsheets().values().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={
                    'valueInputOption': 'USER_ENTERED',
                    'data': [
                        {
                            'range': f'{i}!A1:N1',
                            'majorDimension': 'ROWS',
                            'values': [self.columns],
                        }
                    ],
                },
            ).execute()

    @staticmethod
    def get_sheet_name(direction):
        if direction == 'Аналитика':
            # self.global_1_row += 1
            return 'Аналитика'
        elif direction == 'ML':
            # self.global_2_row += 1
            return 'ML'
        elif direction in ('Product Management', 'Project  Management'):
            # self.global_3_row += 1
            return 'Product Project'
        else:
            # self.global_0_row += 1
            return 'Разработка'

    @classmethod
    def extract_dataframe(cls, data: list[ParseResultDTO]):
        sheets_data = {
            'Разработка': [],
            'Аналитика': [],
            'ML': [],
            'Product Project': [],
        }
        for i in data:
            sheet_name = cls.get_sheet_name(i.direction)
            sheets_data[sheet_name].append(
                [
                    i.employer,
                    i.title,
                    i.profession,
                    i.exp,
                    i.skills,
                    i.salary,
                    i.tech_flag,
                    i.manager_flag,
                    i.salary_range,
                    i.desc,
                    i.work_format,
                    i.city,
                    i.link,
                ]
            )
        return sheets_data

    def save_many_vacancies(self, data: list[ParseResultDTO]):
        sheets_data = self.extract_dataframe(data)
        sending_data = []
        for i in self.sheets:
            sending_data.append(
                {
                    'range': f'{i}!A2',
                    'values': sheets_data[i],
                }
            )
        self.sheet_service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                'valueInputOption': 'RAW',
                'data': sending_data,
            },
        ).execute()


if __name__ == '__main__':
    google_storage = GoogleStorage(settings.GOOGLE_API_KEY)
    print(google_storage.get_spreadsheet_link())

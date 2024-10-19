import json
import logging
import os
import tempfile
import time

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
        self.get_settings_spreadsheet()
        self.delete_all()
        self.create_column_names(self.columns)

    def delete_all(self):
        self.create_column_names(['' for i in range(15)])
        spreadsheet_data = []
        for i in range(len(self.sheets)):
            spreadsheet_data.append(
                {'deleteDimension': {'range': {'sheetId': i, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 14}}}
            )

        self.sheet_service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id, body={'requests': spreadsheet_data}
        ).execute()

    def get_spreadsheet_link(self):
        return f'https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}'

    def auth(self, api_file):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            json.dump(api_file, temp_file, indent=4)
            temp_file_path = temp_file.name

        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
            temp_file_path,
            ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'],
        )
        os.remove(temp_file_path)
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

    def get_settings_spreadsheet(self):
        self.spreadsheet_id = settings.GOOGLE_SPREADSHEET_ID
        if not settings.INCLUDE_PREVIOUS:
            self.spreadsheet_id = settings.GOOGLE_SPREADSHEET_ID_VACANCIES

    def add_permissions(self, permissions):
        self.service = apiclient.discovery.build('drive', 'v3', http=self.httpAuth)
        for i in permissions:
            self.service.permissions().create(
                fileId=settings.GOOGLE_SPREADSHEET_ID,
                body={'sendNotificationEmails': False, 'type': 'user', 'role': 'writer', 'emailAddress': i},
                fields='id',
            ).execute()
        for i in permissions:
            self.service.permissions().create(
                fileId=settings.GOOGLE_SPREADSHEET_ID_VACANCIES,
                body={'sendNotificationEmails': False, 'type': 'user', 'role': 'writer', 'emailAddress': i},
                fields='id',
            ).execute()

    def send_data(self, sending_data, n=0):
        if n >= 10:
            return
        try:
            self.sheet_service.spreadsheets().values().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body={
                    'valueInputOption': 'RAW',
                    'data': sending_data,
                },
            ).execute()
        except Exception as e:
            logging.error(f'Error while saving into google: {e}')
            time.sleep(30 + n)
            self.send_data(sending_data, n + 1)

    def create_column_names(self, columns):
        sending_data = []
        for i in self.sheets:
            sending_data.append(
                {
                    'range': f'{i}!A1',
                    'values': [columns],
                }
            )
        self.send_data(sending_data)

    @staticmethod
    def get_sheet_name(direction):
        if direction == 'Аналитика':
            return 'Аналитика'
        elif direction == 'ML':
            return 'ML'
        elif direction in ('Product Management', 'Project  Management'):
            return 'Product Project'
        else:
            return 'Разработка'

    @classmethod
    def extract_dataframe(cls, data: list[ParseResultDTO]):
        sheets_data = {
            'Разработка': [],
            'Аналитика': [],
            'ML': [],
            'Product Project': [],
        }
        count = 0
        for i in data:
            if i.profession is None or i.profession == '':
                continue
            count += 1
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
        return sheets_data, count

    def save_many_vacancies(self, data: list[ParseResultDTO]):
        sheets_data, count = self.extract_dataframe(data)
        sending_data = []
        for i in self.sheets:
            sending_data.append(
                {
                    'range': f'{i}!A2',
                    'values': sheets_data[i],
                }
            )
        self.send_data(sending_data)
        return count


if __name__ == '__main__':
    google_storage = GoogleStorage('google-api-key.json')
    print(google_storage.get_spreadsheet_link())

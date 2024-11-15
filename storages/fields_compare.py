from urls_crowler.dto import ParseResultDTO


class FieldCompare:
    columns_dev = [
        'Компания',
        'Должность',
        'Поднаправление',
        'Стек',
        'Требуемый опыт',
        'Грэйд',
        'Ссылка',
        'Описание',
        'ЗП',
        'Формат',
        'Город',
    ]
    columns_an = [
        'Компания',
        'Должность',
        'Поднаправление',
        'Грэйд',
        'Город',
        'Формат',
        'Стек',
        'Описание',
        'Ссылка',
    ]
    columns_ml = [
        'Компания',
        'Должность',
        'Поднаправление',
        'Требуемый опыт',
        'Грэйд',
        'Город',
        'Формат',
        'Стек',
        'ЗП',
        'Тех образование',
        'Опыт управления',
        'Диапозон ЗП',
        'Описание',
        'Ссылка',
    ]
    columns_pr = [
        'Компания',
        'Должность',
        'Поднаправление',
        'Грэйд',
        'Город',
        'Формат',
        'ЗП',
        'Ссылка',
    ]

    @staticmethod
    def field_compare(column: str, page_data: ParseResultDTO):
        field_compare = {
            'Компания': page_data.employer,
            'Должность': page_data.title,
            'Поднаправление': page_data.profession,
            'Требуемый опыт': page_data.exp,
            'Стек': page_data.skills,
            'ЗП': page_data.salary,
            'Тех образование': page_data.tech_flag,
            'Опыт управления': page_data.manager_flag,
            'Диапозон ЗП': page_data.salary_range,
            'Описание': page_data.desc,
            'Формат': page_data.work_format,
            'Город': page_data.city,
            'Ссылка': page_data.link,
            'Грэйд': page_data.grade,
        }
        return field_compare[column]

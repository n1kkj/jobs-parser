import pandas

from urls_crowler.dto import ParseResultDTO


def extract_dataframe(page_data: ParseResultDTO) -> pandas.DataFrame:
    dataframe = pandas.DataFrame(
        [
            [
                page_data.employer,
                page_data.title,
                page_data.exp,
                page_data.skills,
                page_data.salary,
                page_data.desc,
                page_data.city,
                page_data.link,
            ]
        ],
        columns=['Компания', 'Должность', 'Требуемый опыт', 'Стек', 'ЗП', 'Описание', 'Город', 'Ссылка'],
    )

    return dataframe

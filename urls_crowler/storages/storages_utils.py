import pandas

from urls_crowler.dto import ParseResultDTO


def extract_dataframe(page_data: ParseResultDTO) -> pandas.DataFrame:
    dataframe = pandas.DataFrame(
        [
            [
                page_data.title,
                page_data.desc,
                page_data.skills,
                page_data.salary,
                page_data.city,
                page_data.employer,
                page_data.link,
            ]
        ],
        columns=['title', 'desc', 'skills', 'salary', 'city', 'employer', 'link'],
    )

    return dataframe

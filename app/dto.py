from dataclasses import dataclass


@dataclass
class PageData:
    url: str
    vacancy_name: str
    vacancy_description: str
    vacancy_source: str | None

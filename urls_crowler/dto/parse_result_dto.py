from typing import Optional

from pydantic import BaseModel


class ParseResultDTO(BaseModel):
    title: Optional[str]
    desc: Optional[str]
    skills: Optional[str]
    exp: Optional[str]
    salary: Optional[str]
    city: Optional[str]
    employer: Optional[str]
    direction: Optional[str]
    profession: Optional[str]
    link: str

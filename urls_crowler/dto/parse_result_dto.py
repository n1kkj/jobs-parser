from pydantic import BaseModel
from typing import Optional


class ParseResultDTO(BaseModel):
    title: Optional[str]
    desc: Optional[str]
    skills: Optional[str]
    exp: Optional[str]
    salary: Optional[str]
    city: Optional[str]
    employer: Optional[str]
    link: str

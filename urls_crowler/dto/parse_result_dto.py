from pydantic import BaseModel
from typing import Optional


class ParseResultDTO(BaseModel):
    title: Optional[str]
    desc: Optional[str]
    skills: Optional[str]
    salary: Optional[str]
    city: Optional[str]
    employer: Optional[str]

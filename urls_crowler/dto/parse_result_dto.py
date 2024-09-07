from typing import Optional, List

from pydantic import BaseModel, Field


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
    work_format: Optional[str]
    link: str
    users: Optional[List[int]] = []

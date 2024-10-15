from typing import Optional, List

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
    work_format: Optional[str]
    tech_flag: Optional[bool]
    manager_flag: Optional[bool]
    salary_range: Optional[str]
    link: Optional[str]
    users: Optional[List[int]] = []

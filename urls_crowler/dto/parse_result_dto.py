from typing import Optional, List

from pydantic import BaseModel


class ParseResultDTO(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None
    skills: Optional[str] = None
    exp: Optional[str] = None
    salary: Optional[str] = None
    city: Optional[str] = None
    employer: Optional[str] = None
    direction: Optional[str] = None
    profession: Optional[str] = None
    work_format: Optional[str] = None
    tech_flag: Optional[bool] = None
    manager_flag: Optional[bool] = None
    salary_range: Optional[str] = None
    link: Optional[str] = None
    users: Optional[List[int]] = []

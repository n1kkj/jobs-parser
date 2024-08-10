from pydantic import BaseModel
from typing import Optional


class FixedValuesDTO(BaseModel):
    title: Optional[str]
    desc: Optional[str]
    salary: Optional[str]
    city: Optional[str]
    employer: Optional[str]

from pydantic import BaseModel, Field
from typing import Optional


class FixedValuesDTO(BaseModel):
    title: Optional[str] = Field(None)
    desc: Optional[str] = Field(None)
    salary: Optional[str] = Field(None)
    exp: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    employer: Optional[str] = Field(None)

from typing import Optional

from pydantic import BaseModel


class ResultMessageDTO(BaseModel):
    all_links_count: int
    time_spent: str
    av_speed: int
    google_link: Optional[str]

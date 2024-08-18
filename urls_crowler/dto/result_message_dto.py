from datetime import datetime

from pydantic import BaseModel


class ResultMessageDTO(BaseModel):
    all_links_count: int
    time_spent: datetime
    av_speed: str

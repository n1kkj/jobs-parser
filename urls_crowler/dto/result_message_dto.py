from pydantic import BaseModel


class ResultMessageDTO(BaseModel):
    all_links_count: int
    time_spent: str
    av_speed: float

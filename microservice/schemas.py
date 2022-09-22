from typing import Optional

from pydantic import BaseModel


class PageStatistics(BaseModel):
    uuid: str
    followers_count: Optional[int]
    posts_count:  Optional[int]

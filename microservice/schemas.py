from typing import Optional

from pydantic import BaseModel


class PageStatisticsBase(BaseModel):
    uuid: str


class CreatePageStatistics(PageStatisticsBase):
    owner_username: str


class PageStatistics(PageStatisticsBase):
    owner_username: Optional[str]
    followers_count: Optional[int] = 0
    posts_count:  Optional[int] = 0

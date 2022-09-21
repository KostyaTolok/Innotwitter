from typing import Optional

from pydantic import BaseModel


class PageStatisticsBase(BaseModel):
    uuid: str


class CreatePageStatistics(PageStatisticsBase):
    pass


class PageStatistics(PageStatisticsBase):
    followers_count: Optional[int]
    posts_count:  Optional[int]

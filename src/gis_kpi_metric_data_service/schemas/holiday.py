"""Holiday data transfer schema."""

from datetime import datetime
from pydantic import Field, model_validator
from .base import Schema


class Holiday(Schema):
    id: int = Field(ge=0)
    title: str
    datetime_from: datetime
    datetime_to: datetime

    @model_validator(mode="after")
    def check_interval(self):
        if self.datetime_from.tzinfo is None or self.datetime_to.tzinfo is None:
            raise ValueError("Holiday endpoints must be timezone-aware")
        if self.datetime_to <= self.datetime_from:
            raise ValueError("Holiday end must follow start")
        return self

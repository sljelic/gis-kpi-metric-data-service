"""Date-based holiday contract; interval endpoints are always derived."""

from datetime import date as Date, datetime, time, timedelta
from zoneinfo import ZoneInfo
from pydantic import ConfigDict, Field, model_validator
from .base import Schema


class Holiday(Schema):
    model_config = ConfigDict(from_attributes=True, extra="forbid")
    title: str = Field(min_length=1)
    year: int = Field(ge=1, le=9999)
    date: Date

    @model_validator(mode="after")
    def check_year(self):
        if self.year != self.date.year:
            raise ValueError("Holiday year must match date.year")
        return self

    def interval_bounds(self, timezone="Pacific/Auckland"):
        """Return local midnight boundaries; end is exclusive and DST-safe."""
        zone = ZoneInfo(timezone)
        return (
            datetime.combine(self.date, time(), zone),
            datetime.combine(self.date + timedelta(days=1), time(), zone),
        )

    @property
    def datetime_from(self):
        return self.interval_bounds()[0]

    @property
    def datetime_to(self):
        return self.interval_bounds()[1]

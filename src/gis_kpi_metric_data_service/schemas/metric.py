"""Metric data transfer schema."""

from datetime import datetime, timezone
from pydantic import Field, field_validator
from .base import Schema


class Metric(Schema):
    id: int | None = None
    issue_id: int = Field(ge=0)
    title: str
    value: float | None = Field(default=None, allow_inf_nan=False)
    datetime_calculated: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @field_validator("datetime_calculated")
    @classmethod
    def aware(cls, value):
        if value.tzinfo is None:
            raise ValueError("Calculation timestamp must be timezone-aware")
        return value

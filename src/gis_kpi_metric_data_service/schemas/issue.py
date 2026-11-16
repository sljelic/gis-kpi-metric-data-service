"""Issue data transfer schema."""

from pydantic import AliasChoices, Field, field_validator
from .base import Schema
from .extension import Extension
from .progression import Progression


class Issue(Schema):
    issue_id: int = Field(ge=0, validation_alias=AliasChoices("issue_id", "id"))
    title: str
    type: str | None = None
    class_: str | None = Field(default=None, alias="class")
    date_submitted: int | None = None
    date_resolved: int | None = None
    progressions: list[Progression] = Field(default_factory=list)
    extensions: list[Extension] = Field(default_factory=list)

    @field_validator("type", "class_", mode="before")
    @classmethod
    def object_title(cls, value):
        return (
            value.get("title")
            if isinstance(value, dict)
            else (None if isinstance(value, int) else value)
        )

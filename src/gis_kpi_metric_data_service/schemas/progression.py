"""Progression data transfer schema."""

from .base import Schema


class Progression(Schema):
    against_id: int | None = None
    to_title: str
    date_modified: int

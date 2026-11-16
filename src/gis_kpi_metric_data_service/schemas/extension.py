"""Extension data transfer schema."""

from typing import Any
from .base import Schema


class Extension(Schema):
    link_id: int | None = None
    field_name: str
    value: Any = None

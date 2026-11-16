"""ADMS incident data including its remote Accelo issue identity."""

from pydantic import Field
from .base import Schema


class Incident(Schema):
    incident_id: int = Field(ge=0)
    title: str
    type_id: int
    against_type: str
    against_id: int
    issue_id: int | None = Field(default=None, gt=0)
    date_created_in_accelo: int | None = None
    standing: str | None = None
    status_id: int | None = None
    affiliation_id: int | None = None
    date_started: int | None = None
    date_due: int | None = None
    description: str | None = None
    class_id: int | None = None
    assignee: int | None = None
    priority_id: int | None = None

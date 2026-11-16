"""Incident persistence; the caller owns its transaction and row lock."""

from datetime import datetime, timezone
from ..models.adms.incident import Incident as IncidentModel
from ..schemas.incident import Incident
from .base import CRUDService


class IncidentService(CRUDService):
    model = IncidentModel

    def getById(self, id):
        obj = self.session.get(self.model, id)
        return Incident.model_validate(obj) if obj is not None else None

    def update(self, id, incident):
        values = (
            incident.model_dump(exclude_unset=True)
            if isinstance(incident, Incident)
            else dict(incident)
        )
        values["incident_id"] = id
        return Incident.model_validate(self._save(id, values))

    def create(self, incident):
        id = (
            incident.incident_id
            if isinstance(incident, Incident)
            else incident["incident_id"]
        )
        return self.update(id, incident)

    def mark_ingested(self, id, issue_id, created_at=None):
        issue_id = int(issue_id)
        if issue_id <= 0:
            raise ValueError("Accelo issue_id must be positive")
        obj = self.session.get(self.model, id)
        if obj is None:
            raise ValueError(f"Unknown incident {id}")
        if obj.issue_id is not None and obj.issue_id != issue_id:
            raise ValueError(f"Incident {id} is already linked to another Accelo issue")
        instant = created_at or datetime.now(timezone.utc)
        if instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")
        values = {
            "issue_id": issue_id,
            "date_created_in_accelo": obj.date_created_in_accelo
            if obj.date_created_in_accelo is not None
            else int(instant.timestamp()),
        }
        return Incident.model_validate(self._save(id, values))

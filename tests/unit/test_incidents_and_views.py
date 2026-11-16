from datetime import datetime, timezone
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from gis_kpi_metric_data_service import models as m
from gis_kpi_metric_data_service.schemas.incident import Incident
from gis_kpi_metric_data_service.services.incident import IncidentService


def test_incident_service_links_remote_issue_without_local_issue_row():
    db = create_engine("sqlite://")

    @event.listens_for(db, "connect")
    def attach(connection, _):
        connection.execute("ATTACH DATABASE ':memory:' AS adms")

    m.Incident.__table__.create(db)
    with Session(db) as session, session.begin():
        service = IncidentService(session)
        service.create(
            Incident(
                incident_id=1,
                title="[REF-1] - title",
                type_id=5,
                against_type="company",
                against_id=11,
            )
        )
        stamp = datetime(2026, 1, 1, tzinfo=timezone.utc)
        linked = service.mark_ingested(1, 999, stamp)
        assert linked.issue_id == 999 and linked.date_created_in_accelo == 1767225600
        assert (
            service.mark_ingested(
                1, 999, datetime(2026, 1, 2, tzinfo=timezone.utc)
            ).date_created_in_accelo
            == 1767225600
        )
        service.create(
            Incident(
                incident_id=1,
                title="[REF-1] updated source",
                type_id=5,
                against_type="company",
                against_id=11,
            )
        )
        assert service.getById(1).issue_id == 999
        assert service.getById(1).date_created_in_accelo == 1767225600
        with pytest.raises(ValueError):
            service.mark_ingested(1, 1000, stamp)
        with pytest.raises(ValueError):
            service.mark_ingested(1, 0, stamp)
    db.dispose()


def test_view_is_not_registered_as_a_physical_table():
    assert "public.issues_with_metrics" not in m.Base.metadata.tables
    assert m.IssuesWithMetrics.__table__.name == "issues_with_metrics"
    assert "issue_id" in m.Incident.__table__.columns

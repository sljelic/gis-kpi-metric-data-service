"""Preserve public imports and DTO contracts while implementation modules move."""

from datetime import datetime, timezone
from importlib import import_module
import pickle
import pytest
from pydantic import ValidationError

PREFIX = "gis_kpi_metric_data_service"


@pytest.mark.parametrize(
    "public_module,implementation,name",
    [
        ("schemas", "schemas.base", "Schema"),
        ("schemas", "schemas.holiday", "Holiday"),
        ("schemas", "schemas.progression", "Progression"),
        ("schemas", "schemas.extension", "Extension"),
        ("schemas", "schemas.issue", "Issue"),
        ("schemas", "schemas.metric", "Metric"),
        ("services", "services.base", "CRUDService"),
        ("services", "services.calendar", "CalendarService"),
        ("services", "services.issue", "IssueService"),
        ("services", "services.metric", "MetricService"),
    ],
)
def test_existing_public_import_is_the_same_class(public_module, implementation, name):
    public = import_module(f"{PREFIX}.{public_module}")
    direct = import_module(f"{PREFIX}.{implementation}")
    assert getattr(public, name) is getattr(direct, name)
    assert name in public.__all__


def test_nested_issue_validation_and_serialization_contract():
    from gis_kpi_metric_data_service.schemas import Issue

    issue = Issue(
        id=7,
        title="Example",
        type={"title": "GIS As-built"},
        **{"class": {"title": "Reactive"}},
        progressions=[{"against_id": 7, "to_title": "Open", "date_modified": 0}],
        extensions=[{"link_id": 7, "field_name": "Contractor", "value": "Omexom"}],
    )
    assert (
        issue.issue_id == 7
        and issue.type == "GIS As-built"
        and issue.class_ == "Reactive"
    )
    assert issue.progressions[0].to_title == "Open"
    assert Issue.model_validate_json(issue.model_dump_json()) == issue
    assert pickle.loads(pickle.dumps(issue)) == issue
    assert issue.model_dump(by_alias=True)["class"] == "Reactive"
    assert Issue(issue_id=8, title="Other").extensions == []


def test_timezone_validation_still_applies_through_public_exports():
    from gis_kpi_metric_data_service.schemas import Holiday, Metric

    with pytest.raises(ValidationError):
        Metric(issue_id=1, title="OP2", datetime_calculated=datetime(2026, 1, 1))
    with pytest.raises(ValidationError):
        Holiday(
            id=1,
            title="Invalid",
            datetime_from=datetime(2026, 1, 1),
            datetime_to=datetime(2026, 1, 2),
        )
    metric = Metric(
        issue_id=1,
        title="OP2",
        datetime_calculated=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    assert metric.datetime_calculated.tzinfo is not None


@pytest.mark.parametrize("day,hours", [("2026-04-05", 25), ("2026-09-27", 23)])
def test_holiday_date_contract_and_dst(day, hours):
    from gis_kpi_metric_data_service.schemas import Holiday

    holiday = Holiday(title="DST", year=2026, date=day)
    assert set(holiday.model_dump()) == {"title", "year", "date"}
    start, end = holiday.interval_bounds()
    assert end.timestamp() - start.timestamp() == hours * 3600
    start, end = holiday.interval_bounds("UTC")
    assert end.timestamp() - start.timestamp() == 86400
    assert start.date() == holiday.date
    with pytest.raises(ValidationError):
        Holiday(title="Wrong year", year=2025, date=day)
    with pytest.raises(ValidationError):
        Holiday(title="ID forbidden", year=2026, date=day, id=1)
    with pytest.raises(ValidationError):
        Holiday(title="Endpoints forbidden", year=2026, date=day, datetime_from=start)

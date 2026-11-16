Models, DTOs and services
=========================

Models use the accelo and adms schemas plus the metrics table. JSON columns
retain object-or-ID and dynamic extension values; Unix timestamps use BIGINT.
Python ``class_`` maps to API/database class.

CalendarService, IssueService and MetricService accept a caller-owned
SQLAlchemy Session. They flush but never commit. The caller owns transaction
and connection lifetime. CRUD and AND-combined filters are supported.

IssueService child selectors use None for all, [] for none, and nonempty lists
for matching progression titles/extension field names. Child filtering does
not remove parent issues; link types are constrained to issues. Calculators
need all status transitions to preserve exclusion end timestamps.

Metric snapshots are unique by issue_id, title and datetime_calculated.
MetricService.create reuses that snapshot on retry. Supply the same UTC
calculation timestamp for retries; later runs retain history. CalendarService
uses full local holiday dates, including DST days.

Module boundaries
-----------------

Schemas are defined in schemas/base.py, issue.py, progression.py, extension.py,
holiday.py and metric.py. Services are defined in services/base.py, issue.py,
calendar.py and metric.py. ORM models already have entity/data-source modules.
Package __init__.py files expose public names through re-exports and __all__;
they contain no service or validation implementations.

Existing imports continue to work::

    from gis_kpi_metric_data_service.schemas import Issue
    from gis_kpi_metric_data_service.services import IssueService

Direct module imports are also supported::

    from gis_kpi_metric_data_service.schemas.issue import Issue
    from gis_kpi_metric_data_service.services.issue import IssueService

Services retain their existing names and CRUD API. Their database-query role is
unchanged, and the caller continues to own commit/rollback and session lifetime.


ADMS incident linkage
---------------------

``IncidentService.mark_ingested(id, issue_id, created_at=None)`` updates the remote
ID and ingestion timestamp within the caller's transaction. Existing timestamps
are retained, and conflicting issue IDs are rejected. The Incident schema and ORM
model expose nullable issue_id; no local-issue foreign key is required.

``models.views.IssuesWithMetrics`` is a read-only ORM view with latest pivoted
metrics. Install its physical view using jobs Alembic, then query it with
``session.scalars(select(IssuesWithMetrics))``. It is excluded from table metadata
so create_all/autogeneration cannot accidentally create a table in its place.

Date-based holidays
-------------------

Holiday models and schemas contain only ``title``, ``year`` and ``date``.
The composite primary key is ``(title, year)``; ``year`` must match the date.
``CalendarService.create(holiday)`` atomically upserts by that key, updating the
date on retry. ``getById``, ``update`` and ``delete`` take ``(title, year)``.
The caller owns the transaction. Renaming requires delete/recreate.
CSV imports use ``title,year,date`` without an ID. Run the jobs repository's
Alembic migration before using this version against an existing database.

``Holiday.interval_bounds(timezone)`` derives midnight on the date and midnight
the following day in the requested timezone (Pacific/Auckland by default).
``datetime_from`` and ``datetime_to`` are read-only derived compatibility
properties, excluded from schema serialization and database storage. DST days can
last 23 or 25 hours. No endpoint is accepted from CSV or constructor input.

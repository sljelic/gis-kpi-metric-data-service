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

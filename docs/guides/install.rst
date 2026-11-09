Installation and ownership
==========================

From the repository root, with Python 3.11+ for development::

    python -m venv .venv
    . .venv/bin/activate
    pip install -e '.[dev]'

For PostgreSQL runtime deployments install the ``postgres`` extra.

Ownership:

* ``gis_kpi_metric_data_service.models``: SQLAlchemy models and metadata.
* ``gis_kpi_metric_data_service.schemas``: Pydantic DTOs.
* ``gis_kpi_metric_data_service.services``: session-scoped data services.
* ``gis_kpi_metric_data_service/migrations``: packaged Alembic revision history.
* ``issue-metric-calculator``: calculation strategies using these DTOs.
* ``gis-kpi-metric-jobs``: deployed DAG files, helpers and SQL resources.
* ``gis-kpi-metric-db``: deployment configuration and migration invocation.

This package has no dependency on Airflow or the calculator. The calculator
must depend on this package, not the other way around. Update consumers to
import models/schemas/services from ``gis_kpi_metric_data_service``. The old calculator
persistence import paths have been removed.

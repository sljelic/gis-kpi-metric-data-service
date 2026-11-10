# GIS KPI Persistence

Shared SQLAlchemy models, Pydantic schemas, and services. This is a normal Python library, not an Airflow provider. The database and jobs deployment repositories consume its versioned distribution and are not installed as packages.

```sh
pip install -e '.[dev]'
```

Imports use `gis_kpi_metric_data_service.models`, `.schemas` and `.services`. Revision `0001` is unchanged, so existing migration bookkeeping and data remain valid. Runtime dependencies do not include Airflow or the calculator.

See [REGISTRY.md](REGISTRY.md) for Gitea package publishing, read/write tokens and one-index pip configuration. Provider-style HTML/PDF docs, service tests and wheel-installation checks are included.

## Source organization

ORM models are separated by data source/entity. DTOs live in `schemas/base.py`,
`issue.py`, `progression.py`, `extension.py`, `holiday.py` and `metric.py`.
Database services live in `services/base.py`, `issue.py`, `calendar.py` and
`metric.py`. Their `__init__.py` files contain public re-exports, not implementations.

Both `from gis_kpi_metric_data_service.schemas import Issue` and direct imports
from `schemas.issue` remain supported; service imports are preserved in the same way.

Concrete Alembic revisions and upgrade commands live in [gis-kpi-metric-jobs](https://github.com/sljelic/gis-kpi-metric-jobs).

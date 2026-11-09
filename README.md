# GIS KPI Persistence

Shared SQLAlchemy models, Pydantic schemas, services and packaged Alembic migrations. This is a normal Python library, not an Airflow provider. The database and jobs deployment repositories consume its versioned distribution and are not installed as packages.

```sh
pip install -e '.[dev]'
export GIS_KPI_DATABASE_URL='postgresql+psycopg://user:password@host:5432/gis_kpi'
gis-kpi-metric-data-service upgrade head
```

Imports use `gis_kpi_metric_data_service.models`, `.schemas` and `.services`. Revision `0001` is unchanged, so existing migration bookkeeping and data remain valid. Runtime dependencies do not include Airflow or the calculator.

See [REGISTRY.md](REGISTRY.md) for Gitea package publishing, read/write tokens and one-index pip configuration. Provider-style HTML/PDF docs, service tests, PostgreSQL migration tests and wheel-resource checks are included.

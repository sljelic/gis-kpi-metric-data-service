Python API
==========

The package-level imports remain stable. Each class is implemented in the
entity/responsibility module below; __init__.py files only re-export public names.

Models
------

ORM models remain separated by data source and entity. Importing
``gis_kpi_metric_data_service.models`` registers their tables on
``Base.metadata`` for Alembic; it does not open a database connection.

.. automodule:: gis_kpi_metric_data_service.models.accelo.issues
   :members: Issue

.. automodule:: gis_kpi_metric_data_service.models.accelo.extension_values
   :members: ExtensionValue

.. automodule:: gis_kpi_metric_data_service.models.accelo.issue_progressions
   :members: IssueProgression

.. automodule:: gis_kpi_metric_data_service.models.accelo.holidays
   :members: Holiday

.. automodule:: gis_kpi_metric_data_service.models.adms.incident
   :members: Incident

.. automodule:: gis_kpi_metric_data_service.models.metrics
   :members: Metric

Schemas
-------

.. automodule:: gis_kpi_metric_data_service.schemas.base
   :members: Schema

.. automodule:: gis_kpi_metric_data_service.schemas.issue
   :members: Issue

.. automodule:: gis_kpi_metric_data_service.schemas.progression
   :members: Progression

.. automodule:: gis_kpi_metric_data_service.schemas.extension
   :members: Extension

.. automodule:: gis_kpi_metric_data_service.schemas.holiday
   :members: Holiday

.. automodule:: gis_kpi_metric_data_service.schemas.metric
   :members: Metric

Services
--------

.. automodule:: gis_kpi_metric_data_service.services.base
   :members: CRUDService

.. automodule:: gis_kpi_metric_data_service.services.issue
   :members: IssueService

.. automodule:: gis_kpi_metric_data_service.services.calendar
   :members: CalendarService

.. automodule:: gis_kpi_metric_data_service.services.metric
   :members: MetricService

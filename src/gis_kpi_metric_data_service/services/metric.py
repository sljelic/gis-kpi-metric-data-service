"""MetricService database queries and schema conversion."""

from sqlalchemy import select
from ..models.metrics import Metric as MetricModel
from ..schemas.metric import Metric
from .base import CRUDService


class MetricService(CRUDService):
    model = MetricModel

    @staticmethod
    def _schema(obj):
        # SQLite drops timezone information; persisted instants are UTC.
        from datetime import timezone

        values = {
            k: getattr(obj, k)
            for k in ("id", "issue_id", "title", "value", "datetime_calculated")
        }
        if values["datetime_calculated"].tzinfo is None:
            values["datetime_calculated"] = values["datetime_calculated"].replace(
                tzinfo=timezone.utc
            )
        return Metric(**values)

    def get(self, id=None, issue_id=None, title=None, from_=None, to=None):
        stmt = select(self.model)
        for key, value in [("id", id), ("issue_id", issue_id), ("title", title)]:
            if value is not None:
                stmt = stmt.where(getattr(self.model, key) == value)
        if from_ is not None:
            stmt = stmt.where(self.model.datetime_calculated >= from_)
        if to is not None:
            stmt = stmt.where(self.model.datetime_calculated < to)
        return [
            self._schema(o) for o in self.session.scalars(stmt.order_by(self.model.id))
        ]

    def getById(self, id):
        obj = self.session.get(self.model, id)
        return self._schema(obj) if obj is not None else None

    def create(self, metric):
        # A stable DAG logical timestamp makes retries idempotent.
        obj = self.session.scalar(
            select(self.model).where(
                self.model.issue_id == metric.issue_id,
                self.model.title == metric.title,
                self.model.datetime_calculated == metric.datetime_calculated,
            )
        )
        return self.update(obj.id if obj is not None else metric.id, metric)

    def update(self, id, metric):
        values = metric.model_dump(exclude={"id"})
        from datetime import timezone

        values["datetime_calculated"] = metric.datetime_calculated.astimezone(
            timezone.utc
        )
        if id is not None:
            values["id"] = id
        return self._schema(self._save(id, values))

"""Idempotent calendar operations keyed by (title, year)."""

from datetime import date, datetime
from zoneinfo import ZoneInfo
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from ..models.accelo.holidays import Holiday as HolidayModel
from ..schemas.holiday import Holiday
from .base import CRUDService


class CalendarService(CRUDService):
    model = HolidayModel

    def __init__(self, session, timezone="Pacific/Auckland"):
        super().__init__(session)
        self.zone = ZoneInfo(timezone)

    def _schema(self, obj):
        return Holiday.model_validate(obj)

    def getById(self, key):
        """Read by the composite (title, year) primary key."""
        obj = self.session.get(self.model, key)
        return self._schema(obj) if obj is not None else None

    def _date(self, value):
        if isinstance(value, datetime):
            if value.tzinfo is None:
                raise ValueError("Holiday filter datetime must include a timezone")
            return value.astimezone(self.zone).date()
        if isinstance(value, date):
            return value
        return datetime.fromtimestamp(value, self.zone).date()

    def get(self, year=None, after=None, before=None, titles=None):
        stmt = select(self.model)
        if year is not None:
            stmt = stmt.where(self.model.year == year)
        if after is not None:
            stmt = stmt.where(self.model.date >= self._date(after))
        if before is not None:
            stmt = stmt.where(self.model.date < self._date(before))
        if titles is not None:
            stmt = stmt.where(self.model.title.in_(titles))
        return [
            self._schema(o)
            for o in self.session.scalars(
                stmt.order_by(self.model.date, self.model.title)
            )
        ]

    def create(self, holiday):
        """Upsert without a CSV ID; retries and concurrent imports are safe."""
        holiday = Holiday.model_validate(holiday)
        values = holiday.model_dump()
        dialect = self.session.get_bind().dialect.name
        insert = {"postgresql": pg_insert, "sqlite": sqlite_insert}.get(dialect)
        if insert is None:
            raise NotImplementedError("Calendar upsert requires PostgreSQL or SQLite")
        stmt = insert(self.model).values(**values)
        stmt = stmt.on_conflict_do_update(
            index_elements=[self.model.title, self.model.year],
            set_={"date": stmt.excluded.date},
        )
        self.session.execute(stmt)
        self.session.flush()
        obj = self.session.get(
            self.model, (holiday.title, holiday.year), populate_existing=True
        )
        return self._schema(obj)

    def update(self, key, holiday):
        holiday = Holiday.model_validate(holiday)
        if tuple(key) != (holiday.title, holiday.year):
            raise ValueError(
                "Holiday title/year identify the record; delete and recreate to rename"
            )
        return self.create(holiday)

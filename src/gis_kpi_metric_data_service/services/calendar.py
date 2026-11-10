"""CalendarService database queries and schema conversion."""

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy import select
from ..models.accelo.holidays import Holiday as HolidayModel
from ..schemas.holiday import Holiday
from .base import CRUDService


class CalendarService(CRUDService):
    model = HolidayModel

    def __init__(self, session, timezone="Pacific/Auckland"):
        super().__init__(session)
        self.zone = ZoneInfo(timezone)

    def _schema(self, obj):
        day = datetime.fromtimestamp(obj.date, self.zone).date()
        return Holiday(
            id=obj.id,
            title=obj.title,
            datetime_from=datetime.combine(day, time(), self.zone),
            datetime_to=datetime.combine(day + timedelta(days=1), time(), self.zone),
        )

    def getById(self, id):
        obj = self.session.get(self.model, id)
        return self._schema(obj) if obj is not None else None

    def get(self, year=None, after=None, before=None, titles=None):
        stmt = select(self.model)
        if year is not None:
            stmt = stmt.where(
                self.model.date
                >= int(datetime(year, 1, 1, tzinfo=self.zone).timestamp()),
                self.model.date
                < int(datetime(year + 1, 1, 1, tzinfo=self.zone).timestamp()),
            )
        if after is not None:
            stmt = stmt.where(
                self.model.date >= int(after.timestamp())
                if isinstance(after, datetime)
                else self.model.date >= after
            )
        if before is not None:
            stmt = stmt.where(
                self.model.date < int(before.timestamp())
                if isinstance(before, datetime)
                else self.model.date < before
            )
        if titles is not None:
            stmt = stmt.where(self.model.title.in_(titles))
        return [
            self._schema(o)
            for o in self.session.scalars(stmt.order_by(self.model.date, self.model.id))
        ]

    def create(self, holiday):
        return self.update(holiday.id, holiday)

    def update(self, id, holiday):
        obj = self._save(
            id,
            dict(
                id=id, title=holiday.title, date=int(holiday.datetime_from.timestamp())
            ),
        )
        return self._schema(obj)

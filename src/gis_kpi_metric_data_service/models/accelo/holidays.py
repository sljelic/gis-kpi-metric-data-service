"""Public holidays identified by title and calendar year."""

from sqlalchemy import CheckConstraint, Date, Integer, String, column, extract
from sqlalchemy.orm import mapped_column
from ..base import Base


class Holiday(Base):
    __tablename__ = "holidays"
    __table_args__ = (
        CheckConstraint(
            column("year") == extract("year", column("date")), name="ck_holiday_year"
        ),
        {"schema": "accelo"},
    )
    title = mapped_column(String, primary_key=True)
    year = mapped_column(Integer, primary_key=True)
    date = mapped_column(Date, nullable=False)

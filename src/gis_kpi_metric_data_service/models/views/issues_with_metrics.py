"""Latest OP2/OP3/OP4 values pivoted into one row per issue.

The physical view is created by jobs-owned Alembic revisions, not create_all().
"""

from sqlalchemy import (
    BigInteger,
    Column,
    Float,
    MetaData,
    String,
    Table,
    case,
    func,
    select,
)
from ..base import Base
from ..accelo.issues import Issue
from ..metrics import Metric


def issues_with_metrics_select():
    ranked = (
        select(
            Metric.issue_id,
            Metric.title,
            Metric.value,
            func.row_number()
            .over(
                partition_by=(Metric.issue_id, Metric.title),
                order_by=(Metric.datetime_calculated.desc(), Metric.id.desc()),
            )
            .label("position"),
        )
        .where(Metric.title.in_(["OP2", "OP3", "OP4"]))
        .cte("ranked_metrics")
    )
    pivot = (
        select(
            ranked.c.issue_id,
            *[
                func.max(case((ranked.c.title == name, ranked.c.value))).label(name)
                for name in ["OP2", "OP3", "OP4"]
            ],
        )
        .where(ranked.c.position == 1)
        .group_by(ranked.c.issue_id)
        .cte("pivoted_metrics")
    )
    return select(
        Issue.id,
        Issue.title,
        Issue.class_["title"].as_string().label("class"),
        func.coalesce(
            Issue.issue_type["title"].as_string(), Issue.type["title"].as_string()
        ).label("type"),
        Issue.date_submitted,
        Issue.date_modified,
        Issue.date_resolved,
        pivot.c.OP2,
        pivot.c.OP3,
        pivot.c.OP4,
    ).select_from(Issue.__table__.outerjoin(pivot, Issue.id == pivot.c.issue_id))


# Separate metadata prevents migrations/create_all from mistaking a view for a table.
_view = Table(
    "issues_with_metrics",
    MetaData(),
    Column("id", BigInteger, primary_key=True),
    Column("title", String),
    Column("class", String),
    Column("type", String),
    Column("date_submitted", BigInteger),
    Column("date_modified", BigInteger),
    Column("date_resolved", BigInteger),
    Column("OP2", Float),
    Column("OP3", Float),
    Column("OP4", Float),
    schema="public",
)


class IssuesWithMetrics(Base):
    __table__ = _view
    class_ = _view.c["class"]

"""Read-only database views installed by jobs migrations."""

from .issues_with_metrics import IssuesWithMetrics, issues_with_metrics_select

__all__ = ["IssuesWithMetrics", "issues_with_metrics_select"]

"""IssueService database queries and schema conversion."""

from sqlalchemy import select
from ..models.accelo.issues import Issue as IssueModel
from ..models.accelo.issue_progressions import IssueProgression as IssueProgressionModel
from ..models.accelo.extension_values import ExtensionValue as ExtensionValueModel
from ..schemas.issue import Issue
from ..schemas.progression import Progression
from ..schemas.extension import Extension
from .base import CRUDService


class IssueService(CRUDService):
    model = IssueModel

    def get(
        self,
        modified_after=None,
        modified_before=None,
        class_=None,
        type=None,
        progressions=None,
        extensions=None,
        **filters,
    ):
        class_ = filters.pop("class", class_)
        if filters:
            raise TypeError(f"Unknown filters: {list(filters)}")
        stmt = select(self.model)
        if modified_after is not None:
            stmt = stmt.where(self.model.date_modified > modified_after)
        if modified_before is not None:
            stmt = stmt.where(self.model.date_modified < modified_before)
        if class_ is not None:
            stmt = stmt.where(self.model.class_["title"].as_string() == class_)
        if type is not None:
            # issue_type supersedes deprecated type; fall back only when absent.
            from sqlalchemy import func

            stmt = stmt.where(
                func.coalesce(
                    self.model.issue_type["title"].as_string(),
                    self.model.type["title"].as_string(),
                )
                == type
            )
        return self._schemas(
            list(self.session.scalars(stmt.order_by(self.model.id))),
            progressions,
            extensions,
        )

    def _schemas(self, objects, progressions=None, extensions=None):
        ids = [o.id for o in objects]
        ps, es = {}, {}
        if ids and progressions != []:
            stmt = select(IssueProgressionModel).where(
                IssueProgressionModel.against_id.in_(ids),
                IssueProgressionModel.against_type == "issues",
            )
            if progressions is not None:
                stmt = stmt.where(IssueProgressionModel.to_title.in_(progressions))
            for p in self.session.scalars(
                stmt.order_by(
                    IssueProgressionModel.date_modified, IssueProgressionModel.id
                )
            ):
                if p.date_modified is not None:
                    ps.setdefault(p.against_id, []).append(
                        Progression.model_validate(p)
                    )
        if ids and extensions != []:
            stmt = select(ExtensionValueModel).where(
                ExtensionValueModel.link_id.in_(ids),
                ExtensionValueModel.link_type == "issues",
            )
            if extensions is not None:
                stmt = stmt.where(ExtensionValueModel.field_name.in_(extensions))
            for e in self.session.scalars(stmt.order_by(ExtensionValueModel.id)):
                if e.field_name is not None:
                    es.setdefault(e.link_id, []).append(Extension.model_validate(e))
        return [
            Issue(
                issue_id=o.id,
                title=o.title,
                type=o.issue_type if o.issue_type is not None else o.type,
                class_=o.class_,
                date_submitted=o.date_submitted,
                date_resolved=o.date_resolved,
                progressions=ps.get(o.id, []),
                extensions=es.get(o.id, []),
            )
            for o in objects
        ]

    def getById(self, id, progressions=None, extensions=None):
        obj = self.session.get(self.model, id)
        return (
            self._schemas([obj], progressions, extensions)[0]
            if obj is not None
            else None
        )

    def create(self, issue):
        return self.update(
            issue.get("id") if isinstance(issue, dict) else issue.issue_id, issue
        )

    def update(self, id, issue):
        if isinstance(issue, Issue):
            values = dict(
                id=id,
                title=issue.title,
                issue_type={"title": issue.type} if issue.type else None,
                class_={"title": issue.class_} if issue.class_ else None,
                date_submitted=issue.date_submitted,
                date_resolved=issue.date_resolved,
            )
        else:
            values = dict(issue)
            if "class" in values:
                values["class_"] = values.pop("class")
            values["id"] = id
        obj = self._save(id, values)
        return self._schemas([obj])[0]

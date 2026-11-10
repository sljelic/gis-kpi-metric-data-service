# Changelog

## 0.1.0

- Move persistence models, schemas and services from issue-metric-calculator.
- Keep concrete Alembic history in the jobs repository, preserving revision 0001.

## Unreleased

- Separate DTO schemas and database services into entity/responsibility modules.
- Preserve package-level class imports through explicit public re-exports.
- Document model/migration ownership and deployment-only migration execution.

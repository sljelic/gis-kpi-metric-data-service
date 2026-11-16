# Changelog

## Unreleased

- Add incident issue_id model/schema and transactional ingestion/link service.
- Add a read-only latest OP2/OP3/OP4 pivot view model, with physical DDL owned by jobs migrations.
- Align extension-value models with the already-existing metadata-column removal revision.

- Separate DTO schemas and database services into entity/responsibility modules.
- Preserve package-level class imports through explicit public re-exports.
- Document model/migration ownership and deployment-only migration execution.

## 0.1.0

- Move persistence models, schemas and services from issue-metric-calculator.
- Keep concrete Alembic history in the jobs repository, preserving revision 0001.

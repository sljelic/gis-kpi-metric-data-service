Development and validation
==========================

The layout follows the provider documentation structure: src for runtime code,
tests/unit and tests/integration, and docs/guides, docs/references,
docs/changelog with one Sphinx configuration.

Run::

    pytest
    python -m build
    python -m twine check dist/*
    make html
    make pdf

SQLite tests exercise service behavior. PostgreSQL migration lifecycle tests
run in the jobs repository.

PDF uses SimplePDF/WeasyPrint and needs Pango plus fonts on the host (Debian:
libpango-1.0-0, libpangoft2-1.0-0, fonts-dejavu-core). Outputs are not tracked.

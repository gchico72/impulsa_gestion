# Copilot / AI Agent Instructions for Impulsa Gestión

Purpose
- Provide focused, actionable guidance so an AI coding assistant can be immediately productive in this Django project.

Big picture
- This is a Django monolith providing management for a school: key apps are `core`, `students`, `teachers`, `subjects`, `courses`, `projects`, and `cooperadora`.
- Business logic that must be testable and decoupled is placed in `*_services` modules (example: `cooperadora/services.py` with `TransactionFactory` and `MonthCloser`).

Key patterns & conventions (concrete examples)
- Domain services: keep heavy business logic in `services.py` modules (e.g. `cooperadora/services.py`). Prefer `apps.get_model()` inside services to avoid circular imports.
- Factories & strategies: the codebase uses explicit factory and strategy classes (see `TransactionFactory`, `CarryoverStrategy`, `MonthCloser` in `cooperadora/services.py`). Follow this pattern when adding domain features.
- Context for templates: the `core.context_processors.user_context` injects `user_roles`, `user_perms`, and `user_groups` used throughout templates (see `templates/base.html`). Use these keys rather than querying request.user in templates.
- Static assets: `impulsa/settings.py` sets `STATICFILES_DIRS` to include `static/` and `graphics/`. Templates apply a cache-busting query param for CSS (`?v=2`)—preserve this pattern when editing `base.html`.
- Settings & env overrides: default uses SQLite (`db.sqlite3`). `impulsa/settings.py` will switch to Postgres when `DATABASE_NAME` and other env vars are present. `DJANGO_SECRET` can be used for dev/test.

Developer workflows (explicit commands)
- Create venv and install (PowerShell):
  - `python -m venv .venv`
  - `.\\.venv\\Scripts\\Activate.ps1`
  - `pip install -r requirements.txt`
- DB/migrations and run server (PowerShell):
  - `py manage.py makemigrations`
  - `py manage.py migrate`
  - `py manage.py createsuperuser`
  - `py manage.py runserver`
- Tests & checks:
  - `py manage.py check`
  - `py manage.py test`
- Useful scripts (run from repo root): `scripts/add_dummy_transactions.py` demonstrates programmatic Django bootstrapping (`os.environ['DJANGO_SETTINGS_MODULE']='impulsa.settings'` + `django.setup()`). Use this pattern for CLI helpers.

Code style & change guidance
- Keep models thin; place domain orchestration in `services.py` as existing apps do.
- Prefer `apps.get_model('app_label', 'ModelName')` when writing reusable service code to avoid circular imports.
- When adding new permissions checks in templates, follow existing `user_perms` checks in `templates/base.html` (e.g., `'subjects.view_subject' in user_perms`).

Integration & deployment notes
- Default dev DB: SQLite file `db.sqlite3` in repo root. Production switches to Postgres via env vars (`DATABASE_NAME`, `DATABASE_USER`, etc.).
- Static files: `collectstatic` is used for production (`py manage.py collectstatic`) and `STATIC_ROOT` is `staticfiles/`.

Files to inspect for context when implementing features
- `impulsa/settings.py` — feature flags, DB switching, static dirs, `LOGIN_URL` and `LOGIN_REDIRECT_URL`.
- `core/context_processors.py` — provides `user_roles`, `user_perms`, used by `templates/base.html`.
- `cooperadora/services.py` — canonical example of service/factory/strategy patterns applied to domain logic.
- `scripts/*.py` — examples of standalone scripts that bootstrap Django (use for data imports or helpers).

Courses module (domain specifics)
- Purpose: manage the institution's courses (ej. primero → tercero), their divisiones and especialidades
  (por ejemplo `Ciencias Naturales`). The UI and domain logic expect:
  - A `Course` model representing a course container (`courses/models.py` defines `Course`).
  - An `Enrollment` model linking `Student` ↔ `Course` (see `courses/models.py`).
- Implementation guidance:
  - If you need to model `level` (primero/segundo/tercero), `division` (A/B/C) or `specialty`
    prefer adding explicit fields or small related models (e.g., `Level`, `Division`, `Specialty`) to keep queries simple.
  - Keep enrollment rules and business flows in a `services.py` (follow the `cooperadora` pattern) — this makes it testable.
  - Use `unique_together` or `UniqueConstraint` for enrollment uniqueness (the repo already uses `unique_together` in `Enrollment.Meta`).
  - Template and view references: check `courses/views.py` and `templates/courses/index.html` for UI examples and permissions checks.
- Permission notes: follow the same permission naming used elsewhere (e.g., `'courses.view_course'` in `user_perms`).

If you change behavior that affects DB schema
- Update migrations via `py manage.py makemigrations` and `py manage.py migrate`.
- Avoid manual SQL changes; prefer Django migrations.

When unsure, follow these heuristics
- Keep logic in `services.py` for testability; models should only hold field definitions and simple helpers.
- Use the `core.context_processors.user_context` keys for permission/role checks in templates.
- For cross-app model references inside services or utilities, use `apps.get_model()` to avoid import cycles.

Questions / feedback
- If something in these notes is unclear or missing (specific scripts, infra, or a custom pattern), tell me which area to expand and I will update this file.

# Core Architecture Rules — HA Irrigation Engine

## Mandatory Principles
- **SOLID**: Strict single responsibility, open/closed extension via adapters, dependency inversion.
- **DRY**: Zero duplicate code or redundant entity definitions.
- **KISS & YAGNI**: Keep implementation simple and avoid dead features.
- **Clean Code**: Full typing, dataclasses, clear names, self-documenting code.

## Strict Restrictions
- **NO TODOs**: Never commit TODO comments or incomplete stubs.
- **NO Placeholders**: Never commit dummy or mock files (e.g. `# Watchdog automation placeholder`).
- **NO Business Logic in Dashboard**: Dashboards are purely presentation layer.
- **NO HA Knowledge in Python Engine Core**: Core Python engine domain model knows only devices and zones, not Sonoff/MQTT/HA entities.
- **NO Vendor Knowledge in Engine**: Vendor specifics live exclusively in `src/adapters/`.

## Quality Deliverable Checklist
Every sprint/task commit must include:
1. Working, tested, production-ready code.
2. Unit tests with 100% pass rate.
3. Updated documentation (`README.md`, `CHANGELOG.md`, `ROADMAP.md`, `PROJECT_STATUS.md`, `DECISIONS.md`).
4. ADRs for any architectural change.
5. Sprint report document (`docs/sprint-XX.md`).
# Project Status — HA Irrigation Engine

## Current Status: Sprint 2 Completed / Sprint 3 Ready

- **Version**: `0.2.0`
- **Active Phase**: Core Framework & Engine Development
- **CI/CD**: GitHub Actions workflow (`.github/workflows/ci.yml`) passing.

## Completed Milestones
- [x] **Sprint 1 (Bootstrap & Documentation)**:
  - Repository structure setup.
  - Complete `.ai/` documentation suite (Single Source of Truth).
  - Development tools (`pyproject.toml`, `requirements-dev.txt`, `ruff`, `pytest`).
  - Core ADRs (`ADR-0001`, `ADR-0002`).
  - Sprint report `docs/sprint-01.md`.
- [x] **Sprint 2 (Registry & Device Adapter System)**:
  - Registry domain models & loader (`src/registry/models.py`, `validator.py`).
  - `ValveAdapter` base class & `SonoffSWVAdapter` entity resolver (`src/adapters/`).
  - Adapter Factory pattern (`src/adapters/factory.py`).
  - Home Assistant Package Generator (`src/build/generator.py`).
  - Modular HA Package (`packages/ha_irrigation_engine.yaml`).
  - Comprehensive unit test suite (`tests/test_registry.py`, `tests/test_adapters.py`, `tests/test_generator.py`).
  - Sprint report `docs/sprint-02.md`.

## Next Sprint
- [ ] **Sprint 3 (Irrigation Engine Core)**: Implementation of `src/engine/engine.py` state machine, zone orchestration, cycle execution, and unit tests.

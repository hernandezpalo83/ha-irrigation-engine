# Changelog — HA Irrigation Engine

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-08-01

### Added
- **Registry Module** (`src/registry/models.py`, `validator.py`): Typed dataclasses and validator for `devices.yaml`, `zones.yaml`, and `settings.yaml`.
- **Adapter Framework** (`src/adapters/base.py`, `sonoff_swv.py`, `factory.py`): Abstract `ValveAdapter` base class and `SonoffSWVAdapter` entity resolver for SONOFF SWV-BSP (Zigbee2MQTT).
- **HA Package Generator** (`src/build/generator.py`): Compiler script generating `packages/ha_irrigation_engine.yaml` from YAML registry.
- **Home Assistant Package** (`packages/ha_irrigation_engine.yaml`): Input helpers, template sensors, and device bindings.
- **ADRs**: Created `ADR-0001` (HA Package Generation Architecture) and `ADR-0002` (Adapter Entity Derivation Strategy).
- **Test Suite** (`tests/test_registry.py`, `tests/test_adapters.py`, `tests/test_generator.py`): Unit tests covering registry loading, validation, entity derivation, and package generation.
- **Documentation**: Expanded `.ai/` documentation suite, `README.md`, `PROJECT_STATUS.md`, `DECISIONS.md`, `docs/sprint-01.md`, and `docs/sprint-02.md`.

## [0.1.0] - 2026-08-01

### Added
- Initial project bootstrap structure.

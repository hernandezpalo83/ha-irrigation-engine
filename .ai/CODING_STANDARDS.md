# Coding Standards — HA Irrigation Engine

## General Principles
- **SOLID**: Maintain clean responsibility separation, interface abstraction, and single responsibility across modules.
- **DRY**: Don't repeat entity derivation logic, YAML definitions, or engine execution states.
- **KISS & YAGNI**: Avoid over-engineering. Do not add unused abstraction layers or unneeded dependencies.
- **Clean Code**: Clear variable naming, strict typing, complete docstrings, no dead code, no TODOs, no placeholders.

## Python Requirements
- **Runtime**: Python 3.12+
- **Typing**: Strict type annotations (`typing`, Dataclasses, Pydantic).
- **Style & Linting**: Standard `ruff` formatting (line length 100).
- **Immutability & State**: Prefer immutable dataclasses (`frozen=True`) for value objects like registry entries and resolved entities.
- **Error Handling**: Custom exception hierarchy inheriting from `IrrigationEngineError`.

## Home Assistant & YAML Standards
- **Schema Validation**: Every user YAML file (`devices.yaml`, `zones.yaml`, `settings.yaml`) must be validated against schema specifications.
- **Naming Conventions**: Snake_case for entity IDs and variables (`switch.riego_huerto`, `binary_sensor.riego_huerto_valve_work_state`).
- **YAML Formatting**: 2-space indentation, clear section headers, descriptive comments.

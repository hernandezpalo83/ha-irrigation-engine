# ADR-0001: HA Package Generation & Registry Validation Architecture

- **Status**: Accepted
- **Date**: 2026-08-01
- **Deciders**: Lead Software Architect

## Context
Home Assistant integrations can become complex when users must manually configure dozens of entities (switches, battery sensors, flow sensors, duration sensors, valve state sensors) for each irrigation valve. 
We need an architecture where users configure only the primary switch entity, while keeping business logic and engine capabilities cleanly decoupled from Home Assistant entity names and protocol specifics (Zigbee, MQTT, Sonoff).

## Decision
We implement a **Python Build Generator & YAML Package Architecture**:
1. **User Registry Configuration**: Users define devices in `registry/devices.yaml`, zones in `registry/zones.yaml`, and global parameters in `registry/settings.yaml`.
2. **Registry Validation**: Python code (`src/registry/validator.py`) parses and strictly validates configuration schemas, verifying entity syntax, unique identifiers, adapter availability, and valid device references in zones.
3. **Adapter Entity Resolution**: Devices bind to a vendor-specific `ValveAdapter` (e.g. `SonoffSWVAdapter`), which derives all child sensor and binary sensor entity IDs from the primary switch.
4. **HA Package Compiler**: The build generator (`src/build/generator.py`) generates a production-ready Home Assistant Package (`packages/ha_irrigation_engine.yaml`) containing input helpers, template sensors, and scripts.

## Consequences
- **Positive**:
  - Zero manual HA configuration for child entities.
  - Zero vendor lock-in; adding new valve vendors requires only a Python adapter subclass.
  - Pure presentation layer on HA side without custom C++ or complex integrations.
- **Negative**:
  - Users must run generator script when modifying `registry/devices.yaml` or reloading HA packages.

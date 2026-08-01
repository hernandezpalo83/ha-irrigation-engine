# ADR-0002: Adapter Entity Derivation & Discovery Pattern

- **Status**: Accepted
- **Date**: 2026-08-01
- **Deciders**: Lead Software Architect

## Context
Different valve hardware models (e.g. SONOFF SWV-BSP, ESPHome custom valves, Shelly Plus 1, Tuya Smart Water Timer) expose different entity structures in Home Assistant. Requiring users to configure 6+ entities per device creates setup friction and configuration errors.

## Decision
We establish a mandatory `ValveAdapter` contract in `src/adapters/base.py`:
- All vendor adapters implement `resolve_entities(switch_entity_id: str) -> ResolvedEntities`.
- `ResolvedEntities` is a strongly-typed dataclass containing:
  - `switch`: Main valve switch entity (`switch.<name>`)
  - `battery`: Battery percentage sensor (`sensor.<name>_battery`)
  - `flow`: Water flow sensor (`sensor.<name>_flow`)
  - `duration`: Real-time duration sensor (`sensor.<name>_real_time_irrigation_duration`)
  - `volume`: Real-time volume sensor (`sensor.<name>_real_time_irrigation_volume`)
  - `status`: Current device status sensor (`sensor.<name>_current_device_status`)
  - `work_state`: Valve work state binary sensor (`binary_sensor.<name>_valve_work_state`)

### SONOFF SWV-BSP Implementation (`SonoffSWVAdapter`)
Derives entities by stripping `switch.` prefix from `switch.riego_<name>` and appending standard Zigbee2MQTT entity suffixes.

## Consequences
- **Positive**:
  - Predictable entity mapping.
  - Automatic entity resolution for Zigbee2MQTT Sonoff SWV valves.
  - Easy extension for future manufacturers via factory pattern (`src/adapters/factory.py`).
- **Negative**:
  - Custom entity names in HA require standard naming conventions or explicit adapter parameters if non-standard Zigbee2MQTT topic names are used.

# Device Support Specification — HA Irrigation Engine

## Overview
HA Irrigation Engine uses an Adapter Pattern to support smart irrigation hardware from any vendor without polluting the core engine logic with vendor-specific entity naming or protocol quirks.

## Standard Resolved Entity Schema
Every `ValveAdapter` implementation accepts a single primary switch entity (`switch.<device_name>`) and derives a standardized mapping of Home Assistant entities:

| Capability / Metric | Target Entity ID Pattern | Type |
|---|---|---|
| Main Valve Switch | `switch.<device_name>` | Switch |
| Battery Percentage | `sensor.<device_name>_battery` | Sensor (%) |
| Flow Rate | `sensor.<device_name>_flow` | Sensor (L/min or m³/h) |
| Real-time Duration | `sensor.<device_name>_real_time_irrigation_duration` | Sensor (min) |
| Real-time Volume | `sensor.<device_name>_real_time_irrigation_volume` | Sensor (L) |
| Device Status | `sensor.<device_name>_current_device_status` | Sensor (enum) |
| Valve Work State | `binary_sensor.<device_name>_valve_work_state` | Binary Sensor (on/off) |

## Supported Devices

### 1. SONOFF SWV-BSP (Zigbee 3.0 via Zigbee2MQTT) — Adapter ID: `sonoff_swv`
- **Primary Switch**: `switch.riego_<name>`
- **Entity Derivation Logic**: Strips domain prefix `switch.` and maps child entities using Zigbee2MQTT standard entity naming scheme:
  - `battery` → `sensor.<object>_battery`
  - `flow` → `sensor.<object>_flow`
  - `duration` → `sensor.<object>_real_time_irrigation_duration`
  - `volume` → `sensor.<object>_real_time_irrigation_volume`
  - `status` → `sensor.<object>_current_device_status`
  - `work_state` → `binary_sensor.<object>_valve_work_state`

### Planned Future Adapters
- **ESPHome**: Adapter for custom ESP32/ESP8266 irrigation controllers.
- **Shelly**: Adapter for Shelly Plus 1 / Shelly Pro valves.
- **Tuya**: Adapter for Tuya Zigbee / Wi-Fi water timers.
- **Generic MQTT**: Customizable adapter mapping JSON payload topics.

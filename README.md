# Home Assistant Irrigation Engine 🌿

[![CI Pipeline](https://github.com/user/ha-irrigation-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/user/ha-irrigation-engine/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blueviolet.svg)](https://www.home-assistant.io/)

A modular, extensible, and production-grade irrigation framework for **Home Assistant**. Designed to support smart water valves across multiple vendors, protocols (Zigbee 3.0, Wi-Fi, MQTT), and integrations (Zigbee2MQTT, ESPHome, Shelly, Tuya).

---

## 🌟 Key Features

- 🔌 **Zero-Configuration Entity Resolution**: Simply register your primary valve switch entity (`switch.riego_huerto`). The engine automatically resolves and monitors flow rate, battery level, irrigation duration, real-time volume, status, and work state sensors.
- 🏭 **Modular Adapter Architecture**: Built-in adapter for **SONOFF SWV-BSP** (Zigbee 3.0 via Zigbee2MQTT), easily extensible for ESPHome, Shelly, Tuya, or Generic MQTT.
- 🛡️ **Safety & Watchdog Protection**: Automatic cutoff timer to prevent flooded lawns or stuck valves.
- 📦 **Home Assistant YAML Packages**: Deploys as clean, non-intrusive Home Assistant package files (`packages/ha_irrigation_engine.yaml`).
- 📊 **Telemetry & Mobile-First Dashboard**: Presentation layer designed with Mushroom, Bubble Card, and ApexCharts.

---

## 🏗️ Frozen Architecture

```
Dashboard (Mushroom / Bubble Card / ApexCharts)
       │
       ▼
Automations Layer (Watchdog / Safety / Notifications)
       │
       ▼
Irrigation Engine Core Logic
       │
       ▼
Device Adapter Layer (Sonoff SWV / ESPHome / Shelly / Tuya)
       │
       ▼
Home Assistant Entities (Switches, Sensors, Binary Sensors)
       │
       ▼
Physical Hardware (Smart Water Valves)
```

---

## 🛠️ Quick Start & Configuration

### 1. Define Devices (`registry/devices.yaml`)
```yaml
version: 1
devices:
  - id: huerto
    name: Huerto
    adapter: sonoff_swv
    switch: switch.riego_huerto
  - id: cesped
    name: Césped
    adapter: sonoff_swv
    switch: switch.riego_cesped
```

### 2. Define Zones (`registry/zones.yaml`)
```yaml
version: 1
zones:
  - id: jardin
    name: Jardín Principal
    devices:
      - huerto
      - cesped
```

### 3. Settings (`registry/settings.yaml`)
```yaml
version: 1
engine:
  watchdog_timeout: 30
  max_irrigation_minutes: 180
```

### 4. Build Package
Generate Home Assistant ready packages:
```bash
python3 -m src.build.generator
```

---

## 🧪 Testing

Run the automated test suite:
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 📄 Documentation & ADRs

- [Architecture Decisions Index (DECISIONS.md)](DECISIONS.md)
- [ADR-0001: Package Generation Architecture](docs/adr/0001-ha-package-generation.md)
- [ADR-0002: Adapter Entity Resolution](docs/adr/0002-adapter-entity-derivation.md)
- [Project Roadmap (ROADMAP.md)](.ai/ROADMAP.md)
- [Project Status (PROJECT_STATUS.md)](PROJECT_STATUS.md)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.

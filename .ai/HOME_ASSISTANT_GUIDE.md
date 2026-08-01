# Home Assistant Guide — HA Irrigation Engine

## Integration Strategy
HA Irrigation Engine integrates into Home Assistant using **YAML Packages** (`packages/ha_irrigation_engine.yaml`), allowing modular installation without requiring custom HACS C++ bindings or breaking updates.

## Package Components
1. **Input Helpers**:
   - `input_number`: Irrigation durations, threshold limits, max safety runtime.
   - `input_boolean`: Engine enabled state, rain skip flag, master override.
   - `input_select`: Manual zone selection, schedule preset select.
2. **Template Sensors**:
   - Engine state summary (`idle`, `irrigating`, `warning`, `error`).
   - Zone aggregated status and remaining duration calculator.
3. **Automations**:
   - Watchdog timer: Automatically closes valves if runtime exceeds configured safety threshold (`settings.yaml`).
   - Irrigation cycle coordinator: Manages sequence, delay between zones, and notifications.
4. **Scripts**:
   - `script.riego_start_device(device_id, duration_minutes)`
   - `script.riego_stop_device(device_id)`
   - `script.riego_stop_all`

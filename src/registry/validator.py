"""Registry validator and loader module."""

import json
from pathlib import Path
from typing import Dict, Any, List, Set, Optional

from .models import DeviceConfig, ZoneConfig, EngineSettings, RegistryData, RegistryValidationError

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def safe_load_yaml(content: str) -> Dict[str, Any]:
    """Parse YAML string using PyYAML if present, or fallback safe parser."""
    if HAS_YAML:
        result = yaml.safe_load(content)
        return result if isinstance(result, dict) else {}

    content = content.strip()
    if not content:
        return {}
    if content.startswith("{"):
        return json.loads(content)

    data: Dict[str, Any] = {}
    current_key: Optional[str] = None
    current_container: Optional[Any] = None

    for line in content.splitlines():
        raw_stripped = line.strip()
        if not raw_stripped or raw_stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip(" "))

        if raw_stripped.startswith("-"):
            item_content = raw_stripped[1:].strip()
            if current_key and isinstance(data.get(current_key), list):
                if ":" in item_content:
                    k, v = item_content.split(":", 1)
                    k = k.strip().strip("'\"")
                    v = v.strip().strip("'\"")
                    item_dict = {k: v}
                    data[current_key].append(item_dict)
                    current_container = item_dict
                else:
                    item_val = item_content.strip("'\"")
                    if item_val.startswith("[") and item_val.endswith("]"):
                        item_val = [x.strip().strip("'\"") for x in item_val[1:-1].split(",") if x.strip()]
                    data[current_key].append(item_val)

        elif ":" in raw_stripped:
            key, val = raw_stripped.split(":", 1)
            key = key.strip().strip("'\"")
            val = val.strip()

            if val.isdigit():
                parsed_val: Any = int(val)
            elif val.lower() == "true":
                parsed_val = True
            elif val.lower() == "false":
                parsed_val = False
            elif val.startswith("[") and val.endswith("]"):
                parsed_val = [x.strip().strip("'\"") for x in val[1:-1].split(",") if x.strip()]
            else:
                parsed_val = val.strip("'\"")

            if indent > 0 and current_key and isinstance(data.get(current_key), dict):
                data[current_key][key] = parsed_val
            elif indent > 0 and isinstance(current_container, dict):
                current_container[key] = parsed_val
            else:
                if val == "":
                    current_key = key
                    if key in ("devices", "zones"):
                        data[key] = []
                    else:
                        data[key] = {}
                else:
                    data[key] = parsed_val
                    current_key = key

    return data


class RegistryValidator:
    """Loads and validates registry YAML files."""

    def __init__(self, registry_dir: Path, available_adapters: Optional[Set[str]] = None) -> None:
        """Initialize RegistryValidator with directory path and optional adapter registry set."""
        self.registry_dir = Path(registry_dir)
        self.available_adapters = available_adapters or {"sonoff_swv"}

    def load_and_validate(self) -> RegistryData:
        """Load all registry files and return validated RegistryData instance.

        Raises:
            RegistryValidationError: If any YAML file is missing, malformed, or breaks business rules.
        """
        devices_file = self.registry_dir / "devices.yaml"
        zones_file = self.registry_dir / "zones.yaml"
        settings_file = self.registry_dir / "settings.yaml"

        devices = self._load_devices(devices_file)
        zones = self._load_zones(zones_file, {d.id for d in devices})
        settings = self._load_settings(settings_file)

        return RegistryData(devices=devices, zones=zones, settings=settings)

    def _load_yaml(self, file_path: Path) -> Dict[str, Any]:
        """Load raw YAML dictionary from file."""
        if not file_path.exists():
            raise RegistryValidationError(f"Required registry file missing: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                parsed = safe_load_yaml(content)
                if not isinstance(parsed, dict):
                    raise RegistryValidationError(f"Invalid YAML content in {file_path}: must be a dictionary")
                return parsed
        except Exception as err:
            raise RegistryValidationError(f"YAML parsing error in {file_path}: {err}") from err

    def _load_devices(self, file_path: Path) -> List[DeviceConfig]:
        """Parse and validate devices.yaml."""
        data = self._load_yaml(file_path)
        devices_list = data.get("devices")
        if not isinstance(devices_list, list) or not devices_list:
            raise RegistryValidationError("devices.yaml must contain a non-empty 'devices' list")

        device_configs: List[DeviceConfig] = []
        seen_ids: Set[str] = set()

        for idx, item in enumerate(devices_list):
            if not isinstance(item, dict):
                raise RegistryValidationError(f"Device item at index {idx} is not a dictionary")

            device_id = item.get("id")
            name = item.get("name")
            adapter = item.get("adapter")
            switch = item.get("switch")

            if not device_id or not isinstance(device_id, str):
                raise RegistryValidationError(f"Device at index {idx} is missing a valid string 'id'")

            if device_id in seen_ids:
                raise RegistryValidationError(f"Duplicate device ID found: '{device_id}'")
            seen_ids.add(device_id)

            if not name or not isinstance(name, str):
                raise RegistryValidationError(f"Device '{device_id}' is missing a valid 'name'")

            if not adapter or adapter not in self.available_adapters:
                raise RegistryValidationError(
                    f"Device '{device_id}' specifies unknown adapter '{adapter}'. "
                    f"Available adapters: {sorted(list(self.available_adapters))}"
                )

            if not switch or not isinstance(switch, str) or not switch.startswith("switch."):
                raise RegistryValidationError(
                    f"Device '{device_id}' has invalid switch entity '{switch}'. Must start with 'switch.'"
                )

            device_configs.append(
                DeviceConfig(id=device_id, name=name, adapter=adapter, switch=switch)
            )

        return device_configs

    def _load_zones(self, file_path: Path, valid_device_ids: Set[str]) -> List[ZoneConfig]:
        """Parse and validate zones.yaml."""
        data = self._load_yaml(file_path)
        zones_list = data.get("zones")
        if not isinstance(zones_list, list) or not zones_list:
            raise RegistryValidationError("zones.yaml must contain a non-empty 'zones' list")

        zone_configs: List[ZoneConfig] = []
        seen_ids: Set[str] = set()

        for idx, item in enumerate(zones_list):
            if not isinstance(item, dict):
                raise RegistryValidationError(f"Zone item at index {idx} is not a dictionary")

            zone_id = item.get("id")
            name = item.get("name")
            devices = item.get("devices")

            if not zone_id or not isinstance(zone_id, str):
                raise RegistryValidationError(f"Zone at index {idx} is missing a valid string 'id'")

            if zone_id in seen_ids:
                raise RegistryValidationError(f"Duplicate zone ID found: '{zone_id}'")
            seen_ids.add(zone_id)

            if not name or not isinstance(name, str):
                raise RegistryValidationError(f"Zone '{zone_id}' is missing a valid 'name'")

            if not isinstance(devices, list) or not devices:
                raise RegistryValidationError(f"Zone '{zone_id}' must specify a non-empty list of device IDs")

            for dev_id in devices:
                if dev_id not in valid_device_ids:
                    raise RegistryValidationError(
                        f"Zone '{zone_id}' references unknown device ID '{dev_id}'"
                    )

            zone_configs.append(ZoneConfig(id=zone_id, name=name, devices=devices))

        return zone_configs

    def _load_settings(self, file_path: Path) -> EngineSettings:
        """Parse and validate settings.yaml."""
        data = self._load_yaml(file_path)
        engine_dict = data.get("engine", {})
        if not isinstance(engine_dict, dict):
            raise RegistryValidationError("settings.yaml 'engine' block must be a dictionary")

        watchdog_timeout = engine_dict.get("watchdog_timeout", 30)
        max_irrigation_minutes = engine_dict.get("max_irrigation_minutes", 180)

        if not isinstance(watchdog_timeout, int) or watchdog_timeout <= 0:
            raise RegistryValidationError("settings.yaml watchdog_timeout must be a positive integer")

        if not isinstance(max_irrigation_minutes, int) or max_irrigation_minutes <= 0:
            raise RegistryValidationError("settings.yaml max_irrigation_minutes must be a positive integer")

        return EngineSettings(
            watchdog_timeout=watchdog_timeout,
            max_irrigation_minutes=max_irrigation_minutes,
        )

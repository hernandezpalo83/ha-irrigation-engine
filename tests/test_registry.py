"""Unit tests for Registry loading and validation."""

import unittest
import tempfile
import shutil
import json
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from src.registry.validator import RegistryValidator
from src.registry.models import RegistryValidationError


class TestRegistryValidator(unittest.TestCase):
    """Test suite for RegistryValidator."""

    def setUp(self) -> None:
        """Create a temporary directory for registry YAML files."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.devices_file = self.test_dir / "devices.yaml"
        self.zones_file = self.test_dir / "zones.yaml"
        self.settings_file = self.test_dir / "settings.yaml"

        # Default valid data
        self.valid_devices = {
            "version": 1,
            "devices": [
                {
                    "id": "huerto",
                    "name": "Huerto",
                    "adapter": "sonoff_swv",
                    "switch": "switch.riego_huerto",
                }
            ],
        }
        self.valid_zones = {
            "version": 1,
            "zones": [
                {
                    "id": "jardin",
                    "name": "Jardín",
                    "devices": ["huerto"],
                }
            ],
        }
        self.valid_settings = {
            "version": 1,
            "engine": {
                "watchdog_timeout": 30,
                "max_irrigation_minutes": 180,
            },
        }

    def tearDown(self) -> None:
        """Remove temporary directory."""
        shutil.rmtree(self.test_dir)

    def _write_yaml(self, path: Path, data: dict) -> None:
        with open(path, "w", encoding="utf-8") as f:
            if HAS_YAML:
                yaml.dump(data, f)
            else:
                f.write(json.dumps(data, indent=2))

    def test_valid_registry_loading(self) -> None:
        """Verify loading a completely valid registry dataset."""
        self._write_yaml(self.devices_file, self.valid_devices)
        self._write_yaml(self.zones_file, self.valid_zones)
        self._write_yaml(self.settings_file, self.valid_settings)

        validator = RegistryValidator(registry_dir=self.test_dir)
        registry_data = validator.load_and_validate()

        self.assertEqual(len(registry_data.devices), 1)
        self.assertEqual(registry_data.devices[0].id, "huerto")
        self.assertEqual(registry_data.devices[0].switch, "switch.riego_huerto")

        self.assertEqual(len(registry_data.zones), 1)
        self.assertEqual(registry_data.zones[0].id, "jardin")

        self.assertEqual(registry_data.settings.watchdog_timeout, 30)

    def test_missing_file_raises_error(self) -> None:
        """Verify error is raised if a required YAML file is missing."""
        self._write_yaml(self.devices_file, self.valid_devices)
        # zones.yaml missing
        validator = RegistryValidator(registry_dir=self.test_dir)
        with self.assertRaises(RegistryValidationError):
            validator.load_and_validate()

    def test_duplicate_device_id_raises_error(self) -> None:
        """Verify duplicate device IDs cause validation failure."""
        invalid_devices = {
            "version": 1,
            "devices": [
                {"id": "huerto", "name": "Huerto 1", "adapter": "sonoff_swv", "switch": "switch.riego_1"},
                {"id": "huerto", "name": "Huerto 2", "adapter": "sonoff_swv", "switch": "switch.riego_2"},
            ],
        }
        self._write_yaml(self.devices_file, invalid_devices)
        self._write_yaml(self.zones_file, self.valid_zones)
        self._write_yaml(self.settings_file, self.valid_settings)

        validator = RegistryValidator(registry_dir=self.test_dir)
        with self.assertRaises(RegistryValidationError) as ctx:
            validator.load_and_validate()
        self.assertIn("Duplicate device ID", str(ctx.exception))

    def test_unknown_adapter_raises_error(self) -> None:
        """Verify specifying an unregistered adapter causes validation failure."""
        invalid_devices = {
            "version": 1,
            "devices": [
                {"id": "huerto", "name": "Huerto", "adapter": "unknown_vendor", "switch": "switch.riego_huerto"},
            ],
        }
        self._write_yaml(self.devices_file, invalid_devices)
        self._write_yaml(self.zones_file, self.valid_zones)
        self._write_yaml(self.settings_file, self.valid_settings)

        validator = RegistryValidator(registry_dir=self.test_dir)
        with self.assertRaises(RegistryValidationError) as ctx:
            validator.load_and_validate()
        self.assertIn("unknown adapter", str(ctx.exception))

    def test_invalid_switch_format_raises_error(self) -> None:
        """Verify switch entity ID not starting with 'switch.' causes validation failure."""
        invalid_devices = {
            "version": 1,
            "devices": [
                {"id": "huerto", "name": "Huerto", "adapter": "sonoff_swv", "switch": "light.riego_huerto"},
            ],
        }
        self._write_yaml(self.devices_file, invalid_devices)
        self._write_yaml(self.zones_file, self.valid_zones)
        self._write_yaml(self.settings_file, self.valid_settings)

        validator = RegistryValidator(registry_dir=self.test_dir)
        with self.assertRaises(RegistryValidationError) as ctx:
            validator.load_and_validate()
        self.assertIn("invalid switch entity", str(ctx.exception))

    def test_zone_referencing_unknown_device_raises_error(self) -> None:
        """Verify zone referencing a non-existent device ID raises validation error."""
        invalid_zones = {
            "version": 1,
            "zones": [
                {"id": "jardin", "name": "Jardín", "devices": ["non_existent_device"]},
            ],
        }
        self._write_yaml(self.devices_file, self.valid_devices)
        self._write_yaml(self.zones_file, invalid_zones)
        self._write_yaml(self.settings_file, self.valid_settings)

        validator = RegistryValidator(registry_dir=self.test_dir)
        with self.assertRaises(RegistryValidationError) as ctx:
            validator.load_and_validate()
        self.assertIn("references unknown device ID", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

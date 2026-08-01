"""Unit tests for Home Assistant Package Generator."""

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

from src.build.generator import PackageGenerator
from src.registry.validator import safe_load_yaml


class TestPackageGenerator(unittest.TestCase):
    """Test suite for PackageGenerator."""

    def setUp(self) -> None:
        self.test_dir = Path(tempfile.mkdtemp())
        self.registry_dir = self.test_dir / "registry"
        self.registry_dir.mkdir()
        self.output_file = self.test_dir / "packages" / "ha_irrigation_engine.yaml"

        devices_data = {
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

        zones_data = {
            "version": 1,
            "zones": [{"id": "jardin", "name": "Jardín", "devices": ["huerto"]}],
        }

        settings_data = {
            "version": 1,
            "engine": {"watchdog_timeout": 45, "max_irrigation_minutes": 120},
        }

        for fname, data in [
            ("devices.yaml", devices_data),
            ("zones.yaml", zones_data),
            ("settings.yaml", settings_data),
        ]:
            with open(self.registry_dir / fname, "w", encoding="utf-8") as f:
                if HAS_YAML:
                    yaml.dump(data, f)
                else:
                    f.write(json.dumps(data, indent=2))

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir)

    def test_generate_package_success(self) -> None:
        """Verify package generation produces valid YAML with correct customization metadata."""
        generator = PackageGenerator(
            registry_dir=self.registry_dir, output_file=self.output_file
        )
        result_path = generator.generate()

        self.assertTrue(result_path.exists())

        with open(result_path, "r", encoding="utf-8") as f:
            content = f.read()
            if HAS_YAML:
                package_data = yaml.safe_load(content)
            else:
                # Remove comment line if present
                clean_lines = [l for l in content.splitlines() if not l.startswith("#")]
                package_data = json.loads("\n".join(clean_lines))

        self.assertIn("homeassistant", package_data)
        self.assertIn("input_boolean", package_data)
        self.assertIn("input_number", package_data)

        # Check customizations
        customize = package_data["homeassistant"]["customize"]
        self.assertIn("switch.riego_huerto", customize)
        device_meta = customize["switch.riego_huerto"]
        self.assertEqual(device_meta["friendly_name"], "Irrigation Valve — Huerto")
        self.assertEqual(device_meta["battery_entity"], "sensor.riego_huerto_battery")
        self.assertEqual(device_meta["flow_entity"], "sensor.riego_huerto_flow")
        self.assertEqual(device_meta["duration_entity"], "sensor.riego_huerto_real_time_irrigation_duration")

        # Check settings initial values
        input_numbers = package_data["input_number"]
        self.assertEqual(input_numbers["riego_watchdog_timeout"]["initial"], 45)
        self.assertEqual(input_numbers["riego_max_duration"]["initial"], 120)


if __name__ == "__main__":
    unittest.main()

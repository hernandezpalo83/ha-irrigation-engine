"""Unit tests for Vendor Adapters and AdapterFactory."""

import unittest
from src.adapters.base import ValveAdapter, ResolvedEntities
from src.adapters.sonoff_swv import SonoffSWVAdapter
from src.adapters.factory import AdapterFactory


class DummyAdapter(ValveAdapter):
    """Dummy adapter for factory registration testing."""

    def resolve_entities(self, switch: str) -> ResolvedEntities:
        return ResolvedEntities(
            switch=switch,
            battery="sensor.dummy_battery",
            flow="sensor.dummy_flow",
            duration="sensor.dummy_duration",
            volume="sensor.dummy_volume",
            status="sensor.dummy_status",
            work_state="binary_sensor.dummy_work_state",
        )


class TestSonoffSWVAdapter(unittest.TestCase):
    """Test suite for SonoffSWVAdapter."""

    def setUp(self) -> None:
        self.adapter = SonoffSWVAdapter()

    def test_entity_resolution_success(self) -> None:
        """Verify correct entity derivation for valid switch entity."""
        switch_id = "switch.riego_huerto"
        resolved = self.adapter.resolve_entities(switch_id)

        self.assertEqual(resolved.switch, "switch.riego_huerto")
        self.assertEqual(resolved.battery, "sensor.riego_huerto_battery")
        self.assertEqual(resolved.flow, "sensor.riego_huerto_flow")
        self.assertEqual(resolved.duration, "sensor.riego_huerto_real_time_irrigation_duration")
        self.assertEqual(resolved.volume, "sensor.riego_huerto_real_time_irrigation_volume")
        self.assertEqual(resolved.status, "sensor.riego_huerto_current_device_status")
        self.assertEqual(resolved.work_state, "binary_sensor.riego_huerto_valve_work_state")

    def test_invalid_switch_prefix_raises_value_error(self) -> None:
        """Verify non-switch entity raises ValueError."""
        with self.assertRaises(ValueError):
            self.adapter.resolve_entities("light.riego_huerto")

    def test_empty_object_id_raises_value_error(self) -> None:
        """Verify switch with empty object_id raises ValueError."""
        with self.assertRaises(ValueError):
            self.adapter.resolve_entities("switch.")


class TestAdapterFactory(unittest.TestCase):
    """Test suite for AdapterFactory."""

    def test_get_registered_adapter(self) -> None:
        """Verify retrieving built-in sonoff_swv adapter."""
        adapter = AdapterFactory.get_adapter("sonoff_swv")
        self.assertIsInstance(adapter, SonoffSWVAdapter)

    def test_get_unknown_adapter_raises_key_error(self) -> None:
        """Verify requesting unregistered adapter raises KeyError."""
        with self.assertRaises(KeyError):
            AdapterFactory.get_adapter("non_existent")

    def test_register_custom_adapter(self) -> None:
        """Verify registering and retrieving a custom adapter class."""
        AdapterFactory.register("dummy", DummyAdapter)
        adapter = AdapterFactory.get_adapter("dummy")
        self.assertIsInstance(adapter, DummyAdapter)
        self.assertIn("dummy", AdapterFactory.available_adapters())


if __name__ == "__main__":
    unittest.main()

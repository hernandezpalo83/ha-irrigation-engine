"""Unit tests for Irrigation Engine core logic."""

import unittest
from src.engine.engine import Engine, IrrigationState, EngineError


class TestEngine(unittest.TestCase):
    """Test suite for Engine domain operations."""

    def setUp(self) -> None:
        self.engine = Engine(max_duration_minutes=180, default_watchdog_timeout=30)

    def test_start_cycle_success(self) -> None:
        """Verify starting an irrigation cycle on an idle device."""
        result = self.engine.start("huerto", 15)
        self.assertEqual(result["event"], "start")
        self.assertEqual(result["device"], "huerto")
        self.assertEqual(result["minutes"], 15)
        self.assertEqual(result["status"], IrrigationState.RUNNING.value)
        self.assertEqual(self.engine.get_status("huerto"), IrrigationState.RUNNING)

    def test_stop_cycle_success(self) -> None:
        """Verify stopping an active irrigation cycle."""
        self.engine.start("huerto", 15)
        result = self.engine.stop("huerto")
        self.assertEqual(result["event"], "stop")
        self.assertEqual(result["device"], "huerto")
        self.assertEqual(result["status"], IrrigationState.IDLE.value)
        self.assertEqual(self.engine.get_status("huerto"), IrrigationState.IDLE)

    def test_start_already_running_raises_error(self) -> None:
        """Verify starting an already running device raises EngineError."""
        self.engine.start("huerto", 15)
        with self.assertRaises(EngineError) as ctx:
            self.engine.start("huerto", 20)
        self.assertIn("already running", str(ctx.exception))

    def test_invalid_duration_zero_raises_error(self) -> None:
        """Verify zero or negative duration raises EngineError."""
        with self.assertRaises(EngineError):
            self.engine.start("huerto", 0)

    def test_exceeding_max_duration_raises_error(self) -> None:
        """Verify duration exceeding max_duration_minutes raises EngineError."""
        with self.assertRaises(EngineError):
            self.engine.start("huerto", 200)

    def test_invalid_device_id_raises_error(self) -> None:
        """Verify empty device ID raises EngineError."""
        with self.assertRaises(EngineError):
            self.engine.start("", 10)


if __name__ == "__main__":
    unittest.main()

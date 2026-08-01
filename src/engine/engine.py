"""Irrigation Engine domain state machine and cycle controller."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any
from datetime import datetime


class IrrigationState(str, Enum):
    """Execution states of the irrigation engine."""

    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"
    SAFETY_CUTOFF = "safety_cutoff"


class EngineError(Exception):
    """Domain exception raised on engine operation failures."""

    pass


@dataclass
class ActiveCycle:
    """Active irrigation cycle tracking details."""

    device_id: str
    target_duration_minutes: int
    start_time: datetime
    elapsed_seconds: int = 0
    status: IrrigationState = IrrigationState.RUNNING


class Engine:
    """Domain engine managing device irrigation states and cycle commands."""

    def __init__(self, max_duration_minutes: int = 180, default_watchdog_timeout: int = 30) -> None:
        """Initialize Irrigation Engine.

        Args:
            max_duration_minutes: Maximum allowed continuous irrigation runtime.
            default_watchdog_timeout: Default watchdog safety cutoff limit.
        """
        self.max_duration_minutes = max_duration_minutes
        self.default_watchdog_timeout = default_watchdog_timeout
        self._active_cycles: Dict[str, ActiveCycle] = {}

    def start(self, device: str, minutes: int) -> Dict[str, Any]:
        """Start irrigation cycle for a target device.

        Args:
            device: Device ID to start.
            minutes: Planned duration in minutes.

        Returns:
            Dictionary payload describing the started event.

        Raises:
            EngineError: If duration is invalid or device is already running.
        """
        if not device or not isinstance(device, str):
            raise EngineError("Device ID must be a non-empty string")

        if minutes <= 0 or minutes > self.max_duration_minutes:
            raise EngineError(
                f"Invalid duration {minutes} min. Must be between 1 and {self.max_duration_minutes} minutes."
            )

        if device in self._active_cycles and self._active_cycles[device].status == IrrigationState.RUNNING:
            raise EngineError(f"Device '{device}' is already running an active cycle")

        cycle = ActiveCycle(
            device_id=device,
            target_duration_minutes=minutes,
            start_time=datetime.now(),
            status=IrrigationState.RUNNING,
        )
        self._active_cycles[device] = cycle

        return {
            "event": "start",
            "device": device,
            "minutes": minutes,
            "status": IrrigationState.RUNNING.value,
        }

    def stop(self, device: str) -> Dict[str, Any]:
        """Stop active irrigation cycle for a target device.

        Args:
            device: Device ID to stop.

        Returns:
            Dictionary payload describing the stopped event.
        """
        if not device or not isinstance(device, str):
            raise EngineError("Device ID must be a non-empty string")

        if device in self._active_cycles:
            del self._active_cycles[device]

        return {
            "event": "stop",
            "device": device,
            "status": IrrigationState.IDLE.value,
        }

    def get_status(self, device: str) -> IrrigationState:
        """Get current state of a device.

        Args:
            device: Device ID.

        Returns:
            IrrigationState enum.
        """
        if device in self._active_cycles:
            return self._active_cycles[device].status
        return IrrigationState.IDLE

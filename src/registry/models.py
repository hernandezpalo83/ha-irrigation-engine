"""Domain data models for HA Irrigation Engine Registry."""

from dataclasses import dataclass, field
from typing import List


class RegistryValidationError(Exception):
    """Exception raised when registry validation fails."""

    pass


@dataclass(frozen=True)
class DeviceConfig:
    """Device registration model.

    Attributes:
        id: Unique identifier for the device.
        name: Human-readable name.
        adapter: Name of the vendor adapter (e.g. 'sonoff_swv').
        switch: Primary switch entity ID in Home Assistant (e.g. 'switch.riego_huerto').
    """

    id: str
    name: str
    adapter: str
    switch: str


@dataclass(frozen=True)
class ZoneConfig:
    """Zone registration model.

    Attributes:
        id: Unique identifier for the zone.
        name: Human-readable zone name.
        devices: List of device IDs associated with this zone.
    """

    id: str
    name: str
    devices: List[str]


@dataclass(frozen=True)
class EngineSettings:
    """Global engine operational settings.

    Attributes:
        watchdog_timeout: Maximum allowed continuous run time in minutes before emergency shutoff.
        max_irrigation_minutes: Maximum programmable single irrigation duration.
    """

    watchdog_timeout: int = 30
    max_irrigation_minutes: int = 180


@dataclass(frozen=True)
class RegistryData:
    """Complete system registry data container."""

    devices: List[DeviceConfig] = field(default_factory=list)
    zones: List[ZoneConfig] = field(default_factory=list)
    settings: EngineSettings = field(default_factory=EngineSettings)

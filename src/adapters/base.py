"""Abstract base class for valve adapters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ResolvedEntities:
    """Dataclass holding all Home Assistant entity IDs resolved for a valve device.

    Attributes:
        switch: Primary valve switch entity ID.
        battery: Battery level sensor entity ID.
        flow: Flow rate sensor entity ID.
        duration: Real-time irrigation duration sensor entity ID.
        volume: Real-time volume sensor entity ID.
        status: Device status sensor entity ID.
        work_state: Valve work state binary sensor entity ID.
    """

    switch: str
    battery: str
    flow: str
    duration: str
    volume: str
    status: str
    work_state: str


class ValveAdapter(ABC):
    """Abstract interface that all device vendor adapters must implement."""

    @abstractmethod
    def resolve_entities(self, switch: str) -> ResolvedEntities:
        """Derive and resolve all secondary entity IDs from the primary switch entity ID.

        Args:
            switch: Primary switch entity ID (e.g. 'switch.riego_huerto').

        Returns:
            ResolvedEntities instance containing all derived entity IDs.

        Raises:
            ValueError: If switch entity ID format is invalid.
        """
        pass

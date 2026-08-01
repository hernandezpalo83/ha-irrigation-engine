"""Adapter implementation for SONOFF SWV-BSP (Zigbee 3.0 via Zigbee2MQTT)."""

from .base import ValveAdapter, ResolvedEntities


class SonoffSWVAdapter(ValveAdapter):
    """Adapter for SONOFF SWV-BSP smart water valve.

    Derives all Zigbee2MQTT entity IDs from a given primary switch entity ID.
    Example input: switch.riego_huerto
    Target outputs:
      - battery: sensor.riego_huerto_battery
      - flow: sensor.riego_huerto_flow
      - duration: sensor.riego_huerto_real_time_irrigation_duration
      - volume: sensor.riego_huerto_real_time_irrigation_volume
      - status: sensor.riego_huerto_current_device_status
      - work_state: binary_sensor.riego_huerto_valve_work_state
    """

    def resolve_entities(self, switch: str) -> ResolvedEntities:
        """Derive secondary entities for SONOFF SWV-BSP valve.

        Args:
            switch: Primary switch entity ID (must start with 'switch.').

        Returns:
            ResolvedEntities dataclass.

        Raises:
            ValueError: If switch is not a valid switch entity string.
        """
        if not isinstance(switch, str) or not switch.startswith("switch."):
            raise ValueError(f"Invalid switch entity ID: '{switch}'. Must start with 'switch.'")

        object_id = switch.split(".", 1)[1]
        if not object_id:
            raise ValueError(f"Invalid switch entity ID: '{switch}'. Object ID cannot be empty.")

        return ResolvedEntities(
            switch=switch,
            battery=f"sensor.{object_id}_battery",
            flow=f"sensor.{object_id}_flow",
            duration=f"sensor.{object_id}_real_time_irrigation_duration",
            volume=f"sensor.{object_id}_real_time_irrigation_volume",
            status=f"sensor.{object_id}_current_device_status",
            work_state=f"binary_sensor.{object_id}_valve_work_state",
        )

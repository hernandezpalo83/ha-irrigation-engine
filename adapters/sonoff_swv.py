from .base import ValveAdapter
class SonoffSWVAdapter(ValveAdapter):
    def resolve_entities(self,switch:str)->dict:
        obj=switch.split('.',1)[1]
        return {
            "switch":switch,
            "battery":f"sensor.{obj}_battery",
            "flow":f"sensor.{obj}_flow",
            "duration":f"sensor.{obj}_real_time_irrigation_duration",
            "volume":f"sensor.{obj}_real_time_irrigation_volume",
            "status":f"sensor.{obj}_current_device_status",
            "work_state":f"binary_sensor.{obj}_valve_work_state",
        }

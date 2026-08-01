from .base import ValveAdapter
class SonoffSWVAdapter(ValveAdapter):
    def resolve(self, device_id:str)->dict:
        return {
            "switch":f"switch.{device_id}",
            "battery":f"sensor.{device_id}_battery",
            "flow":f"sensor.{device_id}_flow",
        }

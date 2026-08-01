from dataclasses import dataclass
import yaml
@dataclass(frozen=True)
class Device:
    id:str; name:str; adapter:str; switch:str
def load_devices(path):
    data=yaml.safe_load(open(path))
    return [Device(**d) for d in data["devices"]]

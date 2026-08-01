from abc import ABC, abstractmethod
class ValveAdapter(ABC):
    @abstractmethod
    def resolve(self, device_id:str)->dict: ...

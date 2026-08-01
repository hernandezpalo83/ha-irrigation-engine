from abc import ABC, abstractmethod
class ValveAdapter(ABC):
    @abstractmethod
    def resolve_entities(self,switch:str)->dict: ...

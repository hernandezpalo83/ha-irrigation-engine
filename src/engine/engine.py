from enum import Enum
class State(Enum): IDLE="idle"; RUNNING="running"
class Engine:
    def start(self,device,minutes): return {"event":"start","device":device,"minutes":minutes}
    def stop(self,device): return {"event":"stop","device":device}

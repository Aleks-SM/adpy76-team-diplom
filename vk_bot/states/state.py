from enum import Enum


class StateEnum(Enum):
    ASK_AGE_MIN: 0
    ASK_AGE_MAX: 1
    ASK_CITY: 2
    ASK_GENDER: 3
    REGISTERED: 4


class State:
    def init(self):
        return
    
    def feedback(self):
        return

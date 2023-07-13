from enum import IntEnum


class StateEnum(IntEnum):
    ASK_AGE_MIN = 0
    ASK_AGE_MAX = 1
    ASK_CITY = 2
    ASK_GENDER = 3
    REGISTERED = 4

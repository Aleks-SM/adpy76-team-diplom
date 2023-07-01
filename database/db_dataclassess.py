from dataclasses import dataclass


@dataclass
class ClientUser:
    user_id: int
    age_min: int
    age_max: int
    gender: int
    city: str
    state: int


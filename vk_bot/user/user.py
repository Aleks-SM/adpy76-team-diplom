from functools import total_ordering
from enum import IntEnum
from vk_bot.states.enums.state_enum import StateEnum
from database.requests import get_user_data, check_user_exits, get_user_blacklist, set_user_data


class GenderEnum(IntEnum):
    ANY = 0
    FEMALE = 1
    MALE = 2


@total_ordering
class VkUser:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def __lt__(self, other):
        return self.user_id < other.user_id

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __hash__(self):
        return self.user_id


class VkUserClient(VkUser):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.age_min = None
        self.age_max = None
        self.city = None
        self.gender = None
        self.state = None
        self.blacklisted_users = set[int]
        self.try_get_data()

    def try_get_data(self):
        if check_user_exits(self.user_id):
            data = get_user_data(self.user_id)
            if data.state is not None:
                self.state = StateEnum(data.state)
            self.age_min = data.age_min
            self.age_max = data.age_max
            self.city = data.city
            if data.gender is not None:
                self.gender = GenderEnum(data.gender)
            if data.state == StateEnum.REGISTERED:
                self.blacklisted_users = get_user_blacklist(self.user_id)

    def check_next_state(self):
        if self.state == StateEnum.REGISTERED:
            return
        elif self.age_min is None:
            self.state = StateEnum.ASK_AGE_MIN
        elif self.age_max is None:
            self.state = StateEnum.ASK_AGE_MAX
        elif self.city is None:
            self.state = StateEnum.ASK_CITY
        elif self.gender is None:
            self.state = StateEnum.ASK_GENDER
        else:
            self.state = StateEnum.REGISTERED
        set_user_data(self.user_id, {"state": int(self.state)})


class VkUserSearch(VkUser):
    def __init__(self, user_id):
        super().__init__(user_id)
        self.name = ""
        self.profile_link = f"https://vk.com/id{user_id}"
        self.photos = []
        self.related_photos = []
        self.interests = set
        self.age = 0
        self.gender = 0

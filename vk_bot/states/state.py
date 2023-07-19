from vk_api.search import VKSearcherManyUsers, VKSearcherUser
from vk_bot.user.user import VkUserSearch, VkUserClient


class State:
    def __new__(cls, *args, **kwargs):
        if cls is State:
            raise TypeError(f"Only children of '{cls.__name__}' may be instantiated")
        return super().__new__(cls)

    def __init__(self, user_id: int):
        self.user_id = user_id

    async def init(self):
        return

    async def feedback(self):
        return

    @staticmethod
    def int_try_parse(number: str) -> (bool, int):
        try:
            return True, int(number.strip())
        except Exception as e:
            return False, 0

    def try_parse_gender(self, gender: str):
        is_parsed, gender_int = self.int_try_parse(gender)
        if is_parsed and 0 <= gender_int <= 2:
            return True, gender_int
        else:
            return False, 0

    async def get_search_data(self) -> list[VkUserSearch]:
        return list(
            await VKSearcherManyUsers(
                VkUserClient(self.user_id)
            ).search_vk_users_as_client_params()
        )

    async def get_self_interests(self) -> set[str]:
        return await VKSearcherUser(VkUserClient(self.user_id)).get_interests()

    @staticmethod
    async def get_single_user_data(user_id: int) -> VkUserSearch:
        return await VKSearcherUser(user_id).vk_user_search_params()

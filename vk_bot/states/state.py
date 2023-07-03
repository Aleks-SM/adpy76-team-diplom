from enum import Enum
from vk_api.search import VKSearcherManyUsers, VKSearcherUser
from vk_bot.user import VkUserSearch, VkUserClient
from database.requests import get_user_blacklist


class State:
    def __new__(cls, *args, **kwargs):
        if cls is State:
            raise TypeError(f"Only children of '{cls.__name__}' may be instantiated")
        return super().__new__(cls)

    def __init__(self, user_id):
        self.user_id = user_id

    def init(self):
        return
    
    def feedback(self):
        return

    @staticmethod
    def int_try_parse(number: str) -> (bool, int, str):
        try:
            return True, int(number.strip()), ""
        except Exception as e:
            return False, 0, "Пожалуйста, введите число"

    async def get_search_data(self) -> set[VkUserSearch]:
        return await VKSearcherManyUsers(VkUserClient(self.user_id)).search_vk_users_as_client_params()

    async def get_self_interests(self) -> set[str]:
        return await VKSearcherUser(VkUserClient(self.user_id)).get_interests()

    def get_vk_user_interests(self) -> set[str]:
        return VkSearchEngine(VkUserClient(self.user_id)).get_interests()

    def


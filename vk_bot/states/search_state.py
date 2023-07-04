from vk_api.talker import Talker
from vk_bot.states.state import State
from vk_bot.search_cache.search_cache import SearchCache
from vk_bot.user.user import VkUserSearch


class SearchState(State):
    def __new__(cls, *args, **kwargs):
        if cls is SearchState:
            raise TypeError(f"Only children of '{cls.__name__}' may be instantiated")
        return super().__new__(cls)

    def __init__(self, user_id: int, search_cache: SearchCache):
        super().__init__(user_id)
        self.search_cache = search_cache

    def send_user_search(self):
        user_search = self.search_cache.pop_queue(self.user_id)
        if user_search is not VkUserSearch:
            user_search = self.get_single_user_data(user_search)
        Talker(self.user_id).vk_search_user(user_search)

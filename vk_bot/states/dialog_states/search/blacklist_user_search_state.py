from vk_bot.states.search_state import SearchState
from database.requests import set_blacklist_user
from vk_bot.search_cache.search_cache import SearchCache


class BlacklistUserSearchState(SearchState):
    def __init__(self, user_id: int, search_cache: SearchCache):
        super().__init__(user_id, search_cache)

    async def feedback(self):
        last_user = await self.get_last_user_search()
        if last_user is not None:
            set_blacklist_user(self.user_id, last_user)
        await self.send_user_search()

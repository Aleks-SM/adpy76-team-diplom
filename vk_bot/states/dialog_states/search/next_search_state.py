from vk_bot.states.search_state import SearchState
from vk_bot.search_cache.search_cache import SearchCache


class NextSearchState(SearchState):
    def __init__(self, user_id: int, search_cache: SearchCache):
        super().__init__(user_id, search_cache)

    async def feedback(self, message=""):
        await self.send_user_search()





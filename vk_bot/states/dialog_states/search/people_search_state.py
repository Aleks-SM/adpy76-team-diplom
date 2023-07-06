from vk_bot.states.search_state import SearchState
from vk_bot.search_cache.search_cache import SearchCache


class PeopleSearch(SearchState):
    def __init__(self, user_id: int, search_cache: SearchCache):
        super().__init__(user_id, search_cache)

    async def feedback(self):
        search_users = await self.get_search_data()
        self.search_cache.add_new_queue(self.user_id, search_users)
        await self.send_user_search()
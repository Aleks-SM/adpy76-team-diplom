from vk_bot.states.search_state import SearchState
from database.requests import get_user_favorites
from vk_bot.search_cache.search_cache import SearchCache


class ShowFavoritesSearchState(SearchState):
    def __init__(self, user_id: int, search_cache: SearchCache):
        super().__init__(user_id, search_cache)

    async def feedback(self, message=""):
        fav_users = list(get_user_favorites(self.user_id))
        self.search_cache.add_new_queue(self.user_id, fav_users)
        await self.send_user_search()

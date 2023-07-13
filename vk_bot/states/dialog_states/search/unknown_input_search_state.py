from vk_api.talker import Talker
from vk_bot.states.search_state import SearchState
from vk_bot.search_cache.search_cache import SearchCache


class UnknownInputSearchState(SearchState):
    def __init__(self, user_id: int, search_cache: SearchCache):
        super().__init__(user_id, search_cache)

    async def feedback(self, message=""):
        await Talker(self.user_id).plain_text_without_buttons("Вы что пытаетесь со мной говорить? Лучше "
                                                              "воспользуйтесь кнопками")
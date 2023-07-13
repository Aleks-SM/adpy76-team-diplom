from vk_bot.states.dialog_states.registration.ask_age_max_state import AskAgeMaxState
from vk_bot.states.dialog_states.registration.ask_age_min_state import AskAgeMinState
from vk_bot.states.dialog_states.registration.ask_city_state import AskCityState
from vk_bot.states.dialog_states.registration.ask_gender_state import AskGenderState
from vk_bot.states.dialog_states.search.blacklist_user_search_state import BlacklistUserSearchState
from vk_bot.states.dialog_states.search.favourite_user_search_state import FavouriteUserSearchState
from vk_bot.states.dialog_states.search.next_search_state import NextSearchState
from vk_bot.states.dialog_states.search.people_search_state import PeopleSearch
from vk_bot.states.dialog_states.search.show_favourites_search_state import ShowFavoritesSearchState
from vk_bot.states.dialog_states.search.unknown_input_search_state import UnknownInputSearchState
from vk_bot.states.enums.state_enum import StateEnum
from vk_bot.states.dialog_states.registration.init_user_state import InitUserState
from vk_bot.enums.menu_button_enums import MenuButtonEnum
from vk_bot.search_cache.search_cache import SearchCache
from vk_bot.user.user import VkUserClient


class VkBot:
    def __init__(self):
        self.search_cache = SearchCache()

    async def action(self, user_id: int, action_type: MenuButtonEnum, message=""):
        user = VkUserClient(user_id)
        state = self.get_state(user, action_type, message)
        await state.feedback(message)
        user.try_get_data()
        state = self.get_state(user, action_type, message)
        await state.init()

    def get_search_action_state(self, user_id, action_type: MenuButtonEnum, message):
        match action_type:
            case MenuButtonEnum.NEXT:
                return NextSearchState(user_id, self.search_cache)
            case MenuButtonEnum.SHOW_FAVORITES:
                return ShowFavoritesSearchState(user_id, self.search_cache)
            case MenuButtonEnum.BLOCK_USER:
                return BlacklistUserSearchState(user_id, self.search_cache)
            case MenuButtonEnum.LIKE:
                return FavouriteUserSearchState(user_id, self.search_cache)
            case MenuButtonEnum.SEARCH:
                return PeopleSearch(user_id, self.search_cache)
            case MenuButtonEnum.PLAIN_TEXT:
                return UnknownInputSearchState(user_id, self.search_cache)

    def get_state(self, user: VkUserClient, action_type: MenuButtonEnum, message):
        user_id = user.user_id
        match user.state:
            case StateEnum.REGISTERED:
                return self.get_search_action_state(user_id, action_type, message)
            case StateEnum.ASK_AGE_MIN:
                return AskAgeMinState(user_id)
            case StateEnum.ASK_AGE_MAX:
                return AskAgeMaxState(user_id)
            case StateEnum.ASK_CITY:
                return AskCityState(user_id)
            case StateEnum.ASK_GENDER:
                return AskGenderState(user_id)
            case None:
                return InitUserState(user_id)





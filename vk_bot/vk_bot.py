from vk_bot.states.enums.state_enum import StateEnum
from vk_bot.states.dialog_states.registration.init_user_state import InitUserState
from vk_bot.enums.menu_button_enums import MenuButtonEnum
from vk_bot.search_cache.search_cache import SearchCache


class VkBot:
    def __init__(self):
        self.search_cache = SearchCache()

    def action(self, user_id: int, action_type: MenuButtonEnum, message=""):
        state = self.perform_user_action(user_id, action_type, message)

    def perform_user_action(self, user_id, action_type: MenuButtonEnum, message):
        match action_type:
            case MenuButtonEnum.NEXT:
                pass
            case MenuButtonEnum.SHOW_FAVORITES:
                pass
            case MenuButtonEnum.BLOCK_USER:
                pass
            case MenuButtonEnum.PLAIN_TEXT:
                return self.plain_text_action(user_id, message)

    def plain_text_action(self, user_id, message):
        match user.state:
            case StateEnum.REGISTERED:
                pass
            case StateEnum.ASK_AGE_MIN:
                pass
            case StateEnum.ASK_AGE_MAX:
                pass
            case StateEnum.ASK_CITY:
                pass
            case StateEnum.ASK_GENDER:
                pass
            case None:
                return InitUserState(user_id)





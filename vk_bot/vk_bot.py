from queue import Queue
from vk_bot.user import VkUserClient, VkUserSearch
from vk_bot.states.state_enum import StateEnum
from vk_bot.states.dialog_states.init_user_state import InitUserState


class ActionEnum:
    PRESSED_NEXT_BUTTON: 0
    PRESSED_SHOW_FAVORITES: 1
    PRESSED_BLOCK_USER: 2
    PLAIN_TEXT: 3


class VkBot:
    def __init__(self):
        self.current_queues = {}

    def action(self, user_id: int, action_type: ActionEnum, message=""):
        state = self.perform_user_action(user_id, action_type, message)

    def perform_user_action(self, user_id, action_type: ActionEnum, message):
        match action_type:
            case ActionEnum.PRESSED_NEXT_BUTTON:
                pass
            case ActionEnum.PRESSED_SHOW_FAVORITES:
                pass
            case ActionEnum.PRESSED_BLOCK_USER:
                pass
            case ActionEnum.PLAIN_TEXT:
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





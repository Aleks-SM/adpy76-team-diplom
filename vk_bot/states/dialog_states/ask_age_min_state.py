from vk_bot.states.state import State
from vk_api.dialog import Talker
from vk_bot.user import VkUserClient
from database.requests import set_user_data


class AskAgeMinState(State):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    def init(self):
        text = "Введите минимальный желаемый возраст"
        Talker(self.user_id).plain_text_without_buttons(text)

    def feedback(self, text=""):
        client = VkUserClient(self.user_id)
        is_parsed, data = self.int_try_parse(text)
        if is_parsed and 14 < data < 100:
            set_user_data(self.user_id, {"age_min": data})
            client.try_get_data()
            client.check_next_state()
            return client.state()
        else:
            text = "Пожалуйста, введите корректный возраст"
            Talker(self.user_id).plain_text_without_buttons(text)
            return None


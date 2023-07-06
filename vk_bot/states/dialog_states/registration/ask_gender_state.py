from vk_bot.states.state import State
from vk_api.talker import Talker
from vk_bot.user.user import VkUserClient
from database.requests import set_user_data


class AskGenderState(State):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    async def init(self):
        text = "Укажите желаемый пол"
        await Talker(self.user_id).gender_request_with_buttons(text)

    def feedback(self, text=""):
        client = VkUserClient(self.user_id)
        is_parsed, data = self.try_parse_gender(text)
        if is_parsed:
            set_user_data(self.user_id, {"gender": data})
            client.try_get_data()
            client.check_next_state()
            return client.state()
        else:
            text = "Упс, не удалось обработать желаемый пол, попробуйте снова"
            await Talker(self.user_id).gender_request_with_buttons(text)
            return None

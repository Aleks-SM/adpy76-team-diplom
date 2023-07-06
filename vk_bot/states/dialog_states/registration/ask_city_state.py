import asyncio

from vk_bot.states.state import State
from vk_api.talker import Talker
from vk_bot.user.user import VkUserClient
from vk_api.tools import check_if_city_exists
from database.requests import set_user_data


class AskCityState(State):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    async def init(self):
        text = "Введите ваш город"
        await Talker(self.user_id).plain_text_without_buttons(text)

    async def feedback(self, text=""):
        client = VkUserClient(self.user_id)
        if check_if_city_exists(text):
            set_user_data(self.user_id, {"city": text})
            client.try_get_data()
            client.check_next_state()
            return client.state()
        else:
            text = "Упс, не удалось найти указанный город, попробуйте снова"
            await Talker(self.user_id).plain_text_without_buttons(text)
            return None

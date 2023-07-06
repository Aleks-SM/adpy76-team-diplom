from vk_bot.states.state import State
from vk_api.talker import Talker
from vk_bot.user.user import VkUserClient
from database.requests import create_user_and_set_data
from vk_api.search import VKSearcherUser


class InitUserState(State):
    def __init__(self, user_id: int):
        super().__init__(user_id)

    def init(self):
        pass

    async def feedback(self, text=""):
        text = "Привет, это бот для поиска новых знакомств!"
        await Talker(self.user_id).plain_text_without_buttons(text)
        data = await self.initiate_user()
        await create_user_and_set_data(data)
        client = VkUserClient(self.user_id)
        client.check_next_state()
        return client.state()

    async def initiate_user(self):
        user = VKSearcherUser(self.user_id)
        await user.vk_user_search_params()
        city = user.city
        data = {"user_id": self.user_id}
        if city is not None:
            data["city"] = city
        return data

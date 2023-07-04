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

    def feedback(self, text=""):
        text = "Привет, это бот для поиска новых знакомств!"
        Talker(self.user_id).plain_text_without_buttons(text)
        data = self.initiate_user()
        create_user_and_set_data(data)
        client = VkUserClient(self.user_id)
        client.check_next_state()
        return client.state()

    def initiate_user(self):
        gender, city = VKSearcherUser(self.user_id).get_info()
        data = {"user_id": self.user_id}
        if gender is not None:
            data["gender"] = gender
        if city is not None:
            data["city"] = city
        return data

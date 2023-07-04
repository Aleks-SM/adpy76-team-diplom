from vk_bot.states.state import State
from vk_api.talker import Talker
from vk_bot.user.user import VkUserClient
from vk_api.search import VKSearcherManyUsers

class PeopleSearch(State):
    def __init__(self, user_id: int, queues: Se):
        super().__init__(user_id)
        self.queues = queues

    def init(self):
        Talker(self.user_id).menu_buttons()

    def feedback(self, show_fav=False):
        client = VkUserClient(self.user_id)
        search_users = await VKSearcherManyUsers(client).search_vk_users_as_client_params()
        self.queues.update({self.user_id: search_users})






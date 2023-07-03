from vk_bot.user import VkUserSearch

class Talker:
    def __init__(self, user_id):
        self.user_id = user_id

    def plain_text_without_buttons(self, message: str):
        pass

    def plain_text_with_buttons(self, message: str):
        pass

    def text_and_vk_search_user_with_buttons(self, message: str, vk_user_data: VkUserSearch):
        pass


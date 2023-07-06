from vk_bot.user.user import VkUserSearch


class Talker:
    def __init__(self, user_id):
        self.user_id = user_id

    async def plain_text_without_buttons(self, message: str):
        pass

    async def plain_text_with_4_buttons(self, message: str):
        pass

    async def vk_search_user(self, vk_user_data: VkUserSearch):
        pass

    async def menu_buttons(self):
        pass

    async def gender_request_with_buttons(self, message: str):
        pass

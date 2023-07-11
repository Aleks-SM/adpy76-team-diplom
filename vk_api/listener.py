import os

from vkbottle.bot import Bot, Message, MessageEvent, rules
from vkbottle_types.events import GroupEventType

from vk_bot.enums.menu_button_enums import MenuButtonEnum
from vk_bot.vk_bot import VkBot

bot = Bot(os.getenv("vk_token"))


class Listener:
    def __init__(self):
        self.vk_bot = VkBot()

    @bot.on.raw_event(
        GroupEventType.MESSAGE_EVENT,
        MessageEvent,
    )
    async def button_action(self, event: MessageEvent):
        action_payload = MenuButtonEnum(int(event.payload["cmd"]))
        await self.vk_bot.action(event.user_id, action_payload)

    @bot.on.message()
    async def plain_text_action(self, message: Message):
        await self.vk_bot.action(message.user_id, MenuButtonEnum.PLAIN_TEXT, message.text)


bot.run_forever()

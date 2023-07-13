from vkbottle.bot import Bot, Message, MessageEvent, rules
from vkbottle_types.events import GroupEventType

from vk_bot.enums.menu_button_enums import MenuButtonEnum
from vk_bot.vk_bot import VkBot
import os

from vkbottle import Bot

bot = Bot(os.getenv("vk_token"))

vk_bot = VkBot()


@bot.on.raw_event(
    GroupEventType.MESSAGE_EVENT,
    MessageEvent,
)
async def button_action(event: MessageEvent):
    action_payload = MenuButtonEnum(int(event.payload["cmd"]))
    await vk_bot.action(event.user_id, action_payload)


@bot.on.private_message()
async def plain_text_action(message: Message):
    await bot.api.messages.send(user_id=message.from_id, message="text", random_id=0)
    await vk_bot.action(message.from_id, MenuButtonEnum.PLAIN_TEXT, message.text)



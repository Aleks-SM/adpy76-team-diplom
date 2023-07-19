import re

from vkbottle.bot import Bot, Message, MessageEvent, rules
from vkbottle_types import GroupTypes
from vkbottle_types.events import GroupEventType

from vk_bot.enums.menu_button_enums import MenuButtonEnum
from vk_bot.states.enums.state_enum import StateEnum
from vk_bot.user.user import VkUserClient
from vk_bot.vk_bot import VkBot
import os

from vkbottle import Bot

bot = Bot(os.getenv("vk_token"))

vk_bot = VkBot()


@bot.on.message()
async def button_action(message: Message):
    if message.payload is not None:
        user = VkUserClient(message.from_id)
        action_payload = int(re.findall(r"\d+", message.payload.split(":")[1])[0])
        if user.state == StateEnum.REGISTERED:
            await vk_bot.action(message.from_id, MenuButtonEnum(action_payload))
        else:
            await vk_bot.action(
                message.from_id, MenuButtonEnum.PLAIN_TEXT, str(action_payload)
            )
    else:
        await vk_bot.action(message.from_id, MenuButtonEnum.PLAIN_TEXT, message.text)


@bot.on.raw_event(
    GroupEventType.MESSAGE_EVENT, MessageEvent, rules.PayloadRule({"cmd": "1"})
)
async def group_join_handler(event: MessageEvent):
    pass

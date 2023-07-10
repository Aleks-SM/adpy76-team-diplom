import os

from vk_bot.user.user import VkUserSearch
from vkbottle.bot import Bot, Message, MessageEvent, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback, GroupEventType


class Talker:
    bot = Bot(token=os.getenv("vk_token"))

    def __init__(self, user_id):
        self.user_id = user_id

    async def plain_text_without_buttons(self, text: str, message: Message, bot=bot):
        await bot.api.messages.send(user_id=self.user_id, message=text)

    async def plain_text_with_4_buttons(self, text: str, bot=bot):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Text("First button"), KeyboardButtonColor.PRIMARY)
            .add(Text('Second button'))
            .add(Text('Third button'), KeyboardButtonColor.NEGATIVE)
            .add(Text("Fourth button"), KeyboardButtonColor.POSITIVE)
            .get_json()
        )
        await bot.api.messages.send(user_id=self.user_id, message=text, keyboard=keyboard)
        return keyboard

    @bot.on.raw_event(GroupEventType.MESSAGE_EVENT, MessageEvent, rules.PayloadRule({"cmd": "search"}))
    async def vk_search_user(self, vk_user_data: VkUserSearch, bot=bot):
        await bot.api.messages.send(
            text=f"Результат поиска\n{vk_user_data.name}\n{vk_user_data.profile_link}"
        )
        for photo in vk_user_data.photos:
            await bot.api.messages.send(attachment=photo)
        if vk_user_data.related_photos:
            for related_photo in vk_user_data.related_photos:
                await bot.api.messages.send(attachment=related_photo)

    async def menu_buttons(self, bot=bot):
        keyboard = (
            Keyboard(inline=False)
            .add(Text("Далее"))
            .add(Text("Лайкнуть"))
            .add(Callback("Поиск", payload={"cmd": "search"}))
            .row()
            .add(Text("Показать избранное"))
            .add(Text("Поместить в черный список"))
            .add(Text("Plain text"))
            .get_json()
        )
        await bot.api.messages.send(user_id=self.user_id, text="ГЛАВНОЕ МЕНЮ", keyboard=keyboard)
        return keyboard

    async def gender_request_with_buttons(self, text: str, bot=bot):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Text("Мужской"), color=KeyboardButtonColor.NEGATIVE)
            .add(Text("Женский"), color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text("Не имеет значения"), color=KeyboardButtonColor.PRIMARY)
            .get_json()
        )
        await bot.api.messages.send(user_id=self.user_id, message=text, keyboard=keyboard)
        return keyboard

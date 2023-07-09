import os

from vk_bot.user.user import VkUserSearch
from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text


class Talker:
    # bot = Bot(token=os.getenv("vk_token"))

    def __init__(self, user_id):
        self.user_id = user_id

    async def plain_text_without_buttons(self, text: str, message: Message):
        await message.answer(text)

    async def plain_text_with_4_buttons(self, text: str, message: Message):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Text("First button"), KeyboardButtonColor.PRIMARY)
            .add(Text('Second button'))
            .add(Text('Third button'), KeyboardButtonColor.NEGATIVE)
            .add(Text("Fourth button"), KeyboardButtonColor.POSITIVE)
        )
        await message.answer(text, keyboard=keyboard)
        return keyboard.get_json()

    async def vk_search_user(self, vk_user_data: VkUserSearch, message: Message):
        await message.answer("Результат поиска")
        await message.answer(vk_user_data.name)
        await message.answer(vk_user_data.profile_link)
        for photo in vk_user_data.photos:
            await message.answer(attachment=photo)
        if vk_user_data.related_photos:
            for related_photo in vk_user_data.related_photos:
                await message.answer(attachment=related_photo)

    async def menu_buttons(self, message: Message):
        keyboard = (
            Keyboard(inline=False)
            .add(Text("Далее"))
            .add(Text("Лайкнуть"))
            .add(Text("Поиск"))
            .row()
            .add(Text("Показать избранное"))
            .add(Text("Поместить в черный список"))
            .add(Text("Plain text"))
            .get_json()
        )
        await message.answer("ГЛАВНОЕ МЕНЮ", keyboard=keyboard)
        return keyboard

    async def gender_request_with_buttons(self, text: str, message: Message):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Text("Мужской"), color=KeyboardButtonColor.NEGATIVE)
            .add(Text("Женский"), color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text("Не имеет значения"), color=KeyboardButtonColor.PRIMARY)
            .get_json()
        )
        await message.answer(text, keyboard=keyboard)
        return keyboard

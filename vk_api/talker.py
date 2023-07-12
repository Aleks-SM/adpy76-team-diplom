import os
import aiohttp

from vk_bot.enums.menu_button_enums import MenuButtonEnum
from vk_bot.user.user import VkUserSearch, GenderEnum
from vkbottle.bot import Bot, Message, MessageEvent, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback, GroupEventType
from vk_api.tools import get_attachment_for_vk_bot


class Talker:
    bot = Bot(token=os.getenv("vk_token"))

    def __init__(self, user_id):
        self.user_id = user_id

    async def plain_text_without_buttons(self, text: str, bot=bot):
        await bot.api.messages.send(user_id=self.user_id, message=text)

    async def plain_text_with_main_buttons(self, text: str, bot=bot):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Callback("Поиск", payload={"cmd": MenuButtonEnum.SEARCH}))
            .add(Callback("Лайк", payload={"cmd": MenuButtonEnum.LIKE}))
            .add(Callback("Блок", payload={"cmd": MenuButtonEnum.BLOCK_USER}))
            .add(Callback("Следующий", payload={"cmd": MenuButtonEnum.NEXT}))
            .add(Callback("Избранные", payload={"cmd": MenuButtonEnum.SHOW_FAVORITES}))
            .get_json()
        )
        await bot.api.messages.send(user_id=self.user_id, message=text, keyboard=keyboard)
        return keyboard

    async def vk_search_user(self, vk_user_data: VkUserSearch, bot=bot):
        await bot.api.messages.send(
            text=f"Результат поиска\n{vk_user_data.name}\n{vk_user_data.profile_link}"
        )
        async with aiohttp.ClientSession as session:
            for photo_link in vk_user_data.photos:
                attachment_photo = await get_attachment_for_vk_bot(
                    session,
                    photo_link,
                    bot,
                    user_id=self.user_id
                )
                await bot.api.messages.send(attachment=attachment_photo, content_source=photo_link)
            if vk_user_data.related_photos:
                for related_photo_link in vk_user_data.related_photos:
                    attachment_related_photo = await get_attachment_for_vk_bot(
                        session,
                        related_photo_link,
                        bot,
                        user_id=self.user_id
                    )
                    await bot.api.messages.send(attachment=attachment_related_photo, content_source=related_photo_link)

    async def menu_buttons(self, bot=bot):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Callback("Поиск", payload={"cmd": MenuButtonEnum.SEARCH}))
            .add(Callback("Лайк", payload={"cmd": MenuButtonEnum.LIKE}))
            .add(Callback("Блок", payload={"cmd": MenuButtonEnum.BLOCK_USER}))
            .add(Callback("Следующий", payload={"cmd": MenuButtonEnum.NEXT}))
            .add(Callback("Избранные", payload={"cmd": MenuButtonEnum.SHOW_FAVORITES}))
            .get_json()
        )
        await bot.api.messages.send(user_id=self.user_id, keyboard=keyboard)
        return keyboard

    async def gender_request_with_buttons(self, text: str, bot=bot):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Callback("Мужской", payload={"cmd": GenderEnum.MALE}))
            .add(Callback("Женский", payload={"cmd": GenderEnum.FEMALE}))
            .row()
            .add(Callback("Не имеет значения", payload={"cmd": GenderEnum.ANY}))
            .get_json()
        )
        await bot.api.messages.send(user_id=self.user_id, message=text, keyboard=keyboard)
        return keyboard

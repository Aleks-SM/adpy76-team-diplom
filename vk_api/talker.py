import os
import aiohttp

from vk_bot.enums.menu_button_enums import MenuButtonEnum
from vk_bot.user.user import VkUserSearch, GenderEnum
from vkbottle.bot import Bot, Message, MessageEvent, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback, GroupEventType
from vk_api.tools import get_attachment_for_vk_bot
from database.database import Database
from datetime import datetime
from vkbottle import Bot


class Talker:
    Database()

    def __init__(self, user_id):
        self.user_id = user_id
        import gc
        self.bot = None
        for obj in gc.get_objects():
            if isinstance(obj, Bot):
                self.bot = obj
                break

    async def plain_text_without_buttons(self, text: str):
        await self.bot.api.messages.send(user_id=self.user_id, message=text, random_id=int(datetime.now().timestamp()))

    async def plain_text_with_main_buttons(self, text: str):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Callback("Поиск", payload={"cmd": MenuButtonEnum.SEARCH}))
            .add(Callback("Лайк", payload={"cmd": MenuButtonEnum.LIKE}))
            .add(Callback("Блок", payload={"cmd": MenuButtonEnum.BLOCK_USER}))
            .add(Callback("Следующий", payload={"cmd": MenuButtonEnum.NEXT}))
            .add(Callback("Избранные", payload={"cmd": MenuButtonEnum.SHOW_FAVORITES}))
            .get_json()
        )
        await self.bot.api.messages.send(
            user_id=self.user_id,
            message=text,
            keyboard=keyboard,
            random_id=int(datetime.now().timestamp())
        )
        return keyboard

    async def vk_search_user(self, vk_user_data: VkUserSearch):
        await self.bot.api.messages.send(
            text=f"Результат поиска\n{vk_user_data.name}\n{vk_user_data.profile_link}"
        )
        async with aiohttp.ClientSession as session:
            for photo_link in vk_user_data.photos:
                attachment_photo = await get_attachment_for_vk_bot(
                    session,
                    photo_link,
                    self.bot,
                    user_id=self.user_id
                )
                await self.bot.api.messages.send(
                    attachment=attachment_photo,
                    content_source=photo_link,
                    random_id=int(datetime.now().timestamp())
                )
            if vk_user_data.related_photos:
                for related_photo_link in vk_user_data.related_photos:
                    attachment_related_photo = await get_attachment_for_vk_bot(
                        session,
                        related_photo_link,
                        self.bot,
                        user_id=self.user_id
                    )
                    await self.bot.api.messages.send(
                        attachment=attachment_related_photo,
                        content_source=related_photo_link,
                        random_id=int(datetime.now().timestamp())
                    )

    async def menu_buttons(self):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Callback("Поиск", payload={"cmd": MenuButtonEnum.SEARCH}))
            .add(Callback("Лайк", payload={"cmd": MenuButtonEnum.LIKE}))
            .add(Callback("Блок", payload={"cmd": MenuButtonEnum.BLOCK_USER}))
            .add(Callback("Следующий", payload={"cmd": MenuButtonEnum.NEXT}))
            .add(Callback("Избранные", payload={"cmd": MenuButtonEnum.SHOW_FAVORITES}))
            .get_json()
        )
        await self.bot.api.messages.send(
            user_id=self.user_id,
            keyboard=keyboard,
            random_id=int(datetime.now().timestamp())
        )
        return keyboard

    async def gender_request_with_buttons(self, text: str):
        keyboard = (
            Keyboard(one_time=True, inline=True)
            .add(Callback("Мужской", payload={"cmd": GenderEnum.MALE}))
            .add(Callback("Женский", payload={"cmd": GenderEnum.FEMALE}))
            .row()
            .add(Callback("Не имеет значения", payload={"cmd": GenderEnum.ANY}))
            .get_json()
        )
        await self.bot.api.messages.send(
            user_id=self.user_id,
            message=text,
            keyboard=keyboard,
            random_id=int(datetime.now().timestamp())
        )
        return keyboard

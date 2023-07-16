import asyncio
import aiohttp

from vk_bot.enums.menu_button_enums import MenuButtonEnum
from vk_bot.user.user import VkUserSearch, GenderEnum
from vkbottle.bot import Bot, Message, MessageEvent, rules
from vkbottle import Keyboard, KeyboardButtonColor, Text, Text, GroupEventType, PhotoMessageUploader, PhotoUploader
from vk_api.tools import get_attachment_for_vk_bot
from vkbottle import Bot


class Talker:

    def __init__(self, user_id):
        self.user_id = user_id
        import gc
        self.bot = None
        for obj in gc.get_objects():
            if isinstance(obj, Bot):
                self.bot = obj
                break

    async def plain_text_without_buttons(self, text: str,):
        await self.bot.api.messages.send(user_id=self.user_id, message=text, random_id=0)

    async def plain_text_with_main_buttons(self, text: str):
        keyboard = (
            Keyboard(one_time=True)
            .add(Text("Поиск", payload={"cmd": MenuButtonEnum.SEARCH.value.__str__()}))
            .add(Text("Лайк", payload={"cmd": MenuButtonEnum.LIKE.value.__str__()}))
            .add(Text("Блок", payload={"cmd": MenuButtonEnum.BLOCK_USER.value.__str__()}))
            .add(Text("Следующий", payload={"cmd": MenuButtonEnum.NEXT.value.__str__()}))
            .add(Text("Избранные", payload={"cmd": MenuButtonEnum.SHOW_FAVORITES.value.__str__()}))
            .get_json()
        )
        await self.bot.api.messages.send(user_id=self.user_id, message=text, keyboard=keyboard, random_id=0)
        return keyboard

    async def vk_search_user(self, vk_user_data: VkUserSearch):
        await self.bot.api.messages.send(
            user_id=self.user_id, message=f"{vk_user_data.name}\n{vk_user_data.profile_link}", random_id=0
        )
        photo_uploader = PhotoMessageUploader(self.bot.api)
        async with aiohttp.ClientSession() as session:
            await self.bot.api.messages.send(user_id=self.user_id, message="Фото из профиля", random_id=0)
            for photo_url in vk_user_data.photos:
                attachment_photo = await get_attachment_for_vk_bot(
                    session=session,
                    photo_url=photo_url,
                    photo_uploader=photo_uploader,
                    user_id=self.user_id
                )
                await self.bot.api.messages.send(user_id=self.user_id, attachment=attachment_photo, random_id=0)
            if vk_user_data.related_photos:
                await self.bot.api.messages.send(user_id=self.user_id, message="Отмечен на фото", random_id=0)
                for related_photo_url in vk_user_data.related_photos:
                    attachment_related_photo = await get_attachment_for_vk_bot(
                        session=session,
                        photo_url=related_photo_url,
                        photo_uploader=photo_uploader,
                        user_id=self.user_id
                    )
                    await asyncio.sleep(0.1)
                    await self.bot.api.messages.send(
                        user_id=self.user_id,
                        attachment=attachment_related_photo, random_id=0
                    )

    async def menu_buttons(self):
        keyboard = (
            Keyboard(one_time=True)
            .add(Text(
                "Поиск",
                payload={"cmd": MenuButtonEnum.SEARCH.value.__str__()}), color=KeyboardButtonColor.PRIMARY
            )
            .add(Text(
                "Лайк",
                payload={"cmd": MenuButtonEnum.LIKE.value.__str__()}), color=KeyboardButtonColor.POSITIVE
            )
            .add(Text(
                "Блок",
                payload={"cmd": MenuButtonEnum.BLOCK_USER.value.__str__()}), color=KeyboardButtonColor.NEGATIVE
            )
            .add(
                Text("Следующий",
                payload={"cmd": MenuButtonEnum.NEXT.value.__str__()}), color=KeyboardButtonColor.SECONDARY
            )
            .add(Text(
                "Избранные",
                payload={"cmd": MenuButtonEnum.SHOW_FAVORITES.value.__str__()})
            )
            .get_json()
        )
        await self.bot.api.messages.send(user_id=self.user_id, keyboard=keyboard, random_id=0, message="💞💞💞")
        return keyboard

    async def gender_request_with_buttons(self, text: str):
        keyboard = (
            Keyboard(one_time=True)
            .add(Text(
                "Мужской",
                payload={"cmd": GenderEnum.MALE.value.__str__()}), color=KeyboardButtonColor.NEGATIVE
            )
            .add(Text(
                "Женский", payload={"cmd": GenderEnum.FEMALE.value.__str__()}),
                color=KeyboardButtonColor.POSITIVE
            )
            .row()
            .add(Text("Не имеет значения", payload={"cmd": GenderEnum.ANY.value.__str__()}))
            .get_json()
        )
        await self.bot.api.messages.send(user_id=self.user_id, message=text, keyboard=keyboard, random_id=0)
        return keyboard

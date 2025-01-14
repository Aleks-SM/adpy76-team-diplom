import asyncio
import os
import pymorphy2
import re
from datetime import datetime
from collections import Counter
from vkbottle import API, VKAPIError
from database.database import Database
from vk_bot.user.user import VkUserSearch, VkUserClient


class VkSearcherEngine:
    Database()

    def __init__(
            self,
            user_id,
            user_api=API(os.getenv("user_token")),
            api=API(os.getenv("vk_token")),
    ):
        self.user_id = user_id
        self.user_api = user_api
        self.api = api
        self.user_params = [
            "first_name",
            "last_name",
            "sex",
            "bdate",
            "city",
            "about",
            "activities" "first_name",
            "last_name",
            "books",
            "games",
            "interests",
            "movies",
            "music",
            "tv",
        ]

    async def parse_user_wall(self, searched_user_id, owners_filter="owner"):
        strings = await self.user_api.wall.get(searched_user_id, filter=owners_filter)
        result_string = []
        morph = pymorphy2.MorphAnalyzer()
        functors_pos = {
            "INTJ",
            "PRCL",
            "CONJ",
            "PREP",
            "VERB",
            "INFN",
            "ADJF",
            "ADJS",
            "GRND",
            "PRTF",
            "PRTS",
            "NPRO",
            "COMP",
            "ADVB",
        }

        for string in strings.items:
            cleanr = re.compile(r"[^А-Яа-яЁёA-Za-z]")
            clean_text = re.sub(cleanr, " ", string.text)
            clean_text_without_spaces = re.sub("\s{2,}", " ", clean_text)

            clean_text_without_spaces.split(" ")
            text = clean_text_without_spaces.lower().lstrip().rstrip()

            words = text.split(" ")
            for word in words:
                if morph.parse(word)[0].tag.POS not in functors_pos:
                    f = ""
                    m = morph.parse(word)[0]
                    if len(m) > 1:
                        f = f + m.normal_form
                    result_string.append(f)
        return set(dict(Counter(result_string).most_common(20)).keys())


class VKSearcherUser(VkSearcherEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.user_id = user_id
        self.name: str = ""
        self.profile_link: str = f"https://vk.com/id{self.user_id}"
        self.photos = []
        self.related_photos = []
        self.interests = set
        self.age = 0
        self.city = None
        self.sex = None

    async def get_users_photos(self, searched_user_id, album_id="profile"):
        new_lst = []
        photos = await self.user_api.photos.get(
            searched_user_id, album_id=album_id, extended=True, feed_type="photo"
        )
        lst = []
        for item in photos.items:
            photo = None
            for size in item.sizes:
                photo = size.url
                break
            lst.append((item.likes.count, photo, item.owner_id, item.id))
        if len(lst) > 3:
            lst = sorted(lst, key=lambda x: x[0], reverse=True)[:3]
        for i in lst:
            new_lst.append(i[1])
        if new_lst:
            self.photos = new_lst
        return new_lst

    async def get_related_photos(self, searched_user_id):
        photos_lst = []

        photos = await self.user_api.photos.get_user_photos(searched_user_id)
        for item in photos.items:
            photo = None
            for size in item.sizes:
                photo = size.url
                break
            photos_lst.append(photo)
        return photos_lst

    def prosessing_interests(self, params):
        interests = [
            str(params.about).split(","),
            str(params.activities).split(","),
            str(params.books).split(","),
            str(params.games).split(","),
            str(params.interests).split(","),
            str(params.movies).split(","),
            str(params.music).split(","),
            str(params.tv).split(","),
        ]
        lst = list()
        for _ in interests:
            if len(_) == 1:
                lst.extend(_)
            elif len(_) == 0:
                break
            else:
                for i in _:
                    lst.extend(i)
        return lst

    async def get_interests(self) -> set[str]:
        data = await self.api.users.get(
            user_ids=[self.user_id], fields=self.user_params
        )
        interests = set(self.prosessing_interests(data[0]))
        words_from_wall = await self.parse_user_wall(self.user_id)
        interests.update(words_from_wall)
        return interests

    async def vk_user_search_params(self) -> VkUserSearch:
        user_params = await self.api.users.get(
            user_ids=[self.user_id], fields=self.user_params
        )
        try:
            datetime.strptime(user_params[0].bdate, "%d.%m.%Y").date()
            self.city = user_params[0].city.title
        except:
            self.age = None
            self.city = None
        else:
            self.age = (
                    datetime.now().year
                    - datetime.strptime(user_params[0].bdate, "%d.%m.%Y").date().year
            )
            self.city = user_params[0].city.title
        finally:
            self.name = f"{user_params[0].first_name} {user_params[0].last_name}"
            self.sex = user_params[0].sex.value
            interests = self.prosessing_interests(user_params[0])
            self.interests = set(interests)
            try:
                self.interests.update(await self.parse_user_wall(self.user_id))
            except Exception as e:
                print(e)
            user = VkUserSearch(self.user_id)
            user.name = self.name
            user.interests = self.interests
            user.age = self.age
            user.gender = self.sex
            try:
                photos = await self.get_users_photos(self.user_id)
            except VKAPIError[7]:
                user.photos = []
                self.photos = []
            else:
                user.photos = photos
                self.photos = photos
            try:
                related_photos = await self.get_related_photos(self.user_id)
            except VKAPIError[7]:
                user.related_photos = []
                self.related_photos = []
            else:
                user.related_photos = related_photos
                self.related_photos = related_photos

        return user


class VKSearcherManyUsers(VKSearcherUser):
    def __init__(self, user: VkUserClient, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        user.gender = int(user.gender)
        self.user = user
        self.result: list[VkUserSearch] = []

    async def search_vk_users_as_client_params(self) -> set[VkUserSearch]:
        """Фунция осуществляет поиск по городу, полу, возрасту"""
        # делаем запрос в цикле, чтобы как-то обойти 1000 значений
        for age in range(self.user.age_min, self.user.age_max + 1):
            await asyncio.sleep(0.34)
            peoples = await self.user_api.users.search(
                hometown=self.user.city,
                sex=self.user.gender,
                age_from=age,
                age_to=age,
                has_photo=True,
                is_closed=False,
            )

            for res in peoples.items:
                if not res.is_closed and res.id not in self.user.blacklisted_users:
                    user = VkUserSearch(user_id=res.id)
                    try:
                        if isinstance(res.bdate, str):
                            datetime.strptime(res.bdate, "%d.%m.%Y").date()
                    except ValueError or TypeError:
                        user.age = None
                    else:
                        if isinstance(res.bdate, str):
                            user.age = (
                                    datetime.now().year
                                    - datetime.strptime(res.bdate, "%d.%m.%Y").date().year
                            )
                        else:
                            user.age = None

                    user.name = f"{res.first_name} {res.last_name}"
                    interests = set(self.prosessing_interests(res))
                    await asyncio.sleep(0.2)
                    try:
                        interests.update(await self.parse_user_wall(res.id))
                    except Exception as e:
                        print(e)
                    user.interests = interests
                    await asyncio.sleep(0.34)
                    user.photos = await self.get_users_photos(res.id)
                    await asyncio.sleep(0.2)
                    try:
                        related_photos = await self.get_related_photos(res.id)
                    except VKAPIError[7]:
                        print(
                            f"Пользователь id{self.user.user_id} не имеет прав на получение связанных фото {res.id}"
                        )
                    else:
                        user.related_photos = related_photos

                    self.result.append(user)
        return set(self.result)

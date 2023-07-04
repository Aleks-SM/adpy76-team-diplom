import asyncio
import os
from datetime import datetime
from pprint import pprint

from dotenv import load_dotenv
from vkbottle import API
from database.database import Database
from vk_bot.user import VkUserSearch, VkUserClient


def init_env():
    if os.path.join(os.path.dirname(__file__), ".envrc"):
        path = os.path.split(os.path.dirname(__file__))
        dotenv_path = os.path.join(path[0], ".envrc")
    else:
        dotenv_path = os.path.join(os.path.dirname(__file__), ".envrc")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


class VkSearcherEngine:
    init_env()

    # Database().create_conect()

    def __init__(self, user_id, user_api=API(os.getenv('user_token')), api=API(os.getenv('vk_token'))):
        self.user_id = user_id
        self.user_api = user_api
        self.api = api
        self.user_params = [
            'first_name',
            'last_name',
            'sex',
            'bdate',
            'city',
            'about',
            'activities'
            'first_name',
            'last_name',
            'books',
            'games',
            'interests',
            'movies',
            'music',
            'tv',
        ]


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

    async def get_users_photos(self, album_id='profile'):
        new_lst = []
        photos = await self.user_api.photos.get(
            self.user_id,
            album_id=album_id,
            extended=True,
            feed_type="photo"
        )
        lst = []
        for item in photos.items:
            photo = None
            for size in item.sizes:
                photo = size.url
            lst.append((item.likes.count, photo))

        if len(lst) > 3:
            lst = sorted(lst, key=lambda x: x[0], reverse=True)[:2]

        for i in lst:
            new_lst.append(i[1])

        if new_lst:
            self.photos = new_lst
        return new_lst

    async def get_related_photos(self):
        photos_lst = []
        photos = await self.user_api.photos.get_user_photos(self.user_id)
        for item in photos.items:
            photo = None
            for size in item.sizes:
                photo = size.url
            photos_lst.append(photo)
            return photos_lst

    async def get_interests(self) -> set[str]:
        data = await self.api.users.get(user_ids=[self.user_id], fields=self.user_params)
        params = data[0]
        interests = [
            str(params.about).split(","),
            str(params.activities).split(","),
            str(params.books).split(","),
            str(params.games).split(","),
            str(params.interests).split(","),
            str(params.movies).split(","),
            str(params.music).split(","),
            str(params.tv).split(",")
        ]
        lst = list()
        for _ in interests:
            if len(_) == 1:
                lst.append(*_)
            else:
                for i in _:
                    lst.append(*i)

        return set(lst)

    async def vk_user_search_params(self) -> VkUserSearch:
        user_params = await self.api.users.get(user_ids=[self.user_id], fields=self.user_params)
        params = user_params[0]
        try:
            datetime.strptime(user_params[0].bdate, '%d.%m.%Y').date()
            self.city = user_params[0].city.title
        except ValueError:
            self.age = None
            self.city = None
        else:
            self.age = datetime.now().year - datetime.strptime(user_params[0].bdate, '%d.%m.%Y').date().year
            self.city = user_params[0].city.title
        finally:
            self.name = f'{user_params[0].first_name} {user_params[0].last_name}'
            self.sex = user_params[0].sex.value
            interests = [
                str(params.about).split(","),
                str(params.activities).split(","),
                str(params.books).split(","),
                str(params.games).split(","),
                str(params.interests).split(","),
                str(params.movies).split(","),
                str(params.music).split(","),
                str(params.tv).split(",")
            ]
            lst = list()
            for _ in interests:
                if len(_) == 1:
                    lst.append(*_)
                else:
                    for i in _:
                        lst.append(*i)
            self.interests = set(lst)
            photos = await self.get_users_photos()
            related_photos = await self.get_related_photos()

            user = VkUserSearch(self.user_id)
            user.name = self.name
            user.photos = photos
            self.photos = photos
            user.related_photos = related_photos
            self.related_photos = related_photos
            user.interests = self.interests
            user.age = self.age
            user.gender = self.sex

        return user


class VKSearcherManyUsers(VkSearcherEngine):
    def __init__(self, user: VkUserClient, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.user = user
        self.result: list[VkUserSearch] = []

    async def get_photos_searched_users(self, searched_user_id, album_id='profile'):
        """Функция ищет три или менее самых лайкнутых фотографий из альбома и помещает в список словарей"""

        new_lst = []
        photos = await self.user_api.photos.get(searched_user_id, album_id=album_id, extended=True, feed_type="photo")
        lst = []
        for item in photos.items:
            photo = None
            for size in item.sizes:
                photo = size.url
            lst.append((item.likes.count, photo))
        if len(lst) > 3:
            lst = sorted(lst, key=lambda x: x[0], reverse=True)[:2]
        for i in lst:
            new_lst.append(i[1])
        if new_lst:
            return new_lst

    async def get_related_photos(self, searched_user_id):
        """Получаем связанные с пользователем фотографии. Требуются дополнительные права"""
        photos_lst = []
        photos = await self.user_api.photos.get_user_photos(searched_user_id)
        for item in photos.items:
            photo = None
            for size in item.sizes:
                photo = size.url
            photos_lst.append(photo)
            return photos_lst

    async def search_vk_users_as_client_params(self) -> set[VkUserSearch]:
        """Фунция осуществляет поиск по городу, полу, возрасту"""
        # делаем запрос в цикле, чтобы как-то обойти 1000 значений,
        # здесь можно по дате рождения сделать, тогда значений будет больше, но запрос будет долгим
        for age in range(self.user.age_min, self.user.age_max + 1):
            await asyncio.sleep(0.34)
            peoples = await self.user_api.users.search(
                hometown=self.user.city,
                sex=self.user.gender,
                age_from=age,
                age_to=age,
                has_photo=True,
                is_closed=False
            )

            for res in peoples.items:
                if not res.is_closed and res.id not in self.user.blacklisted_users:
                    user = VkUserSearch(user_id=res.id)
                    try:
                        if isinstance(res.bdate, str):
                            datetime.strptime(res.bdate, '%d.%m.%Y').date()
                    except ValueError or TypeError:
                        user.age = None
                    else:
                        if isinstance(res.bdate, str):
                            user.age = datetime.now().year - datetime.strptime(res.bdate, '%d.%m.%Y').date().year
                        else:
                            user.age = None

                    user.name = f'{res.first_name} {res.last_name}'
                    interests = [
                        res.about.split(','),
                        res.activity.split(','),
                        res.books.split(','),
                        res.games.split(','),
                        res.interests.split(','),
                        res.movies.split(','),
                        res.music.split(',')
                    ]
                    lst = list()
                    for _ in interests:
                        if len(_) == 1:
                            lst.append(*_)
                        else:
                            for i in _:
                                lst.append(*i)
                    user.interests = set(lst)
                    await asyncio.sleep(0.34)
                    user.photos = await self.get_photos_searched_users(res.id)
                    user.related_photos = await self.get_related_photos(res.id)
                    self.result.append(user)
        return set(self.result)


async def test():
    # Здесь тестовая функция. Ее надо удалить
    user_client = VkUserClient(user_id=1)
    user_client.city = "Москва"
    user_client.age_min = 20
    user_client.age_max = 30
    user_client.gender = 1
    user_client.state = 0
    user_searcher = VKSearcherManyUsers(user=user_client)
    user_par = VKSearcherUser(user_id=382668981)
    # await user_searcher.search_vk_users_as_client_params()
    await user_par.vk_user_search_params()
    print(user_par.interests)


asyncio.run(test())

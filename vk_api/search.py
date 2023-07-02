import asyncio
import os
from datetime import datetime
from vkbottle import API
from database.database import Database


class VkSearchEngine:
    Database().create_conect()

    def __init__(
            self,
            user_id: int,
            searched_gender: str = None,
            searched_age_from: int = None,
            searched_age_to: int = None,
            searched_city: str = None,
            interest: str = None,
    ):
        self.user_id = user_id
        self.user_name = None
        self.age = None
        self.sex = None
        self.city = None
        self.searched_gender = searched_gender
        self.searched_city = searched_city
        self.searched_age_from = searched_age_from
        self.searched_age_to = searched_age_to
        self.interest = interest
        self.user_api = API(os.getenv('user_token'))
        self.api = API(os.getenv('vk_token'))
        self.blocked_vk_id: list = []
        self.searched_people = {}
        self.added_photo = []

    async def search_user_params(self):
        fields = [
            'first_name',
            'last_name',
            'sex',
            'bdate',
            'city'
        ]
        user_params = await self.api.users.get(user_ids=[self.user_id], fields=fields)

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
            self.user_name = f'{user_params[0].first_name} {user_params[0].last_name}'
            self.sex = user_params[0].sex.value

    async def search_people_to_meet(self):
        peoples = await self.user_api.users.search(
            hometown=self.searched_city,
            sex=self.searched_gender,
            age_from=self.searched_age_from,
            age_to=self.searched_age_to,
            has_photo=True,
        )

        for res in peoples.items:
            new_lst = []
            if not res.is_closed:
                await asyncio.sleep(0.4)
                photos = await self.user_api.photos.get(res.id, album_id='profile', extended=True, feed_type="photo")
                lst = []
                for item in photos.items:
                    photo = None
                    for size in item.sizes:
                        photo = size.url
                        if size.type.value == "y":
                            photo = size.url
                            break
                    lst.append((item.likes.count, photo))

                if len(lst) > 3:
                    lst = sorted(lst, key=lambda x: x[0], reverse=True)[:2]

                for i in lst:
                    new_lst.append(i[1])

            if new_lst:
                self.searched_people[res.id] = new_lst

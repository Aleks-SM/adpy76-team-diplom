import os
from vkbottle import API
from io import BytesIO


async def check_if_city_exists(city: str) -> bool:
    city = city.capitalize()
    cities_set = set()
    user_api = API(os.getenv("user_token"))
    cities = await user_api.database.get_cities(0, q=city, need_all=True)
    if cities.items:
        for city_name in cities.items:
            if city_name.title == city:
                return True
    #         else:
    #             # если клиент ввел несколько букв своего города, то получит список названий похожих городов
    #             cities_set.add(city_name.title)
    # if cities_set:
    #     print(cities_set)
    #     return cities_set


async def get_attachment_for_vk_bot(session, photo_link, bot, user_id):
    async with session.get(photo_link) as response:
        photo_file = await response.content.read()
        # file = BytesIO(photo_file)
        bot_link = await bot.api.photos.get_messages_upload_server(peer_id=user_id)
        async with session.post(bot_link.upload_url, data=photo_file) as response1:
            data = await response1.json()
            saved_photo = await bot.api.photos.save_messages_photo(
                server=data['server'],
                photo=data['photo'],
                hash=data['hash']
            )
            return f'photo-{saved_photo[3]}_{saved_photo[0]}'

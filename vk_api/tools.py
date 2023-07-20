import os
from vkbottle import API


async def check_if_city_exists(city: str) -> bool:
    city = city.lower()
    cities_set = set()
    user_api = API(os.getenv("user_token"))
    cities = await user_api.database.get_cities(0, q=city, need_all=True)
    if cities.items:
        for city_name in cities.items:
            if city_name.title.lower() == city:
                return True


async def get_attachment_for_vk_bot(session, user_id, photo_url, photo_uploader):
    photo_file = await session.get(photo_url)
    file = await photo_file.content.read()
    photo = await photo_uploader.upload(file_source=file, peer_id=user_id)
    return photo

import os

from vkbottle import API


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

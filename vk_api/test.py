from pprint import pprint

from search import VkSearchEngine
import asyncio


async def test():
    user = VkSearchEngine(
        user_id=1,
        searched_gender=1,
        searched_age_from=20,
        searched_age_to=30,
        searched_city="Москва")

    await asyncio.gather(user.search_user_params(), user.search_people_to_meet())

    pprint(user.city)
    pprint(user.searched_people)


asyncio.run(test())

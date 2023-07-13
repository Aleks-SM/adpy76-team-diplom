from database.database import Database
from database.requests import get_user_data, get_user_blacklist, get_user_favorites, check_user_exits, read_json
from database.requests import create_user_and_set_data, set_user_data, set_blacklist_user, set_favourite_user
from vk_api.listener import bot

if __name__ == "__main__":
    base = Database()
    base.create_tables(base.create_connect())
    bot.run_forever()
    print(get_user_data(1))
    print(get_user_data(999))
    print("{} {}".format("blacklist", get_user_blacklist(1)))
    print("{} {}".format("favorite", get_user_favorites(34)))
    print("{} {}".format("check_user", check_user_exits(1)))
    print("{} {}".format("check_user", check_user_exits(500)))
    print(create_user_and_set_data({"user_id": 123, "gender": 0, "city": "Moscow", "age_min": 20, "age_max": 25}))
    print(set_blacklist_user(1, 777))
    print(set_favourite_user(1, 999))

from database.database import Database
from database.requests import get_user_data, get_user_blacklist, get_user_favorites, check_user_exits, read_json

if __name__ == "__main__":
    base = Database()
    # base.create_tables(base.create_conect())
    # read_json(base.filename)
    print(get_user_data(1))
    print("{} {}".format("blacklist", get_user_blacklist(1)))
    print("{} {}".format("favorite", get_user_favorites(34)))
    print("{} {}".format("check_user", check_user_exits(1)))
    print("{} {}".format("check_user", check_user_exits(500)))
import json
from database.models import User, Favorite, Blacklist
from database.database import Database
from database.db_dataclassess import ClientUser


# Должна возращать ClientUser, если данных нет, то пустые поля должны быть None
def get_user_data(user_id: int) -> ClientUser:
    session = Database().create_session()

    if check_user_exits(user_id):
        for query in session.query(User).filter(User.user_id == user_id).all():
            self = ClientUser(
                user_id=query.user_id,
                age_min=query.search_age_min,
                age_max=query.search_age_max,
                gender=query.search_gender,
                city=query.search_city,
                state=query.state,
            )
    else:
        self = ClientUser(
            user_id=None, age_min=None, age_max=None, gender=None, city=None, state=None
        )
    session.close()
    return self


# Должна возвращать сет из blocked_vk_user_id
def get_user_blacklist(user_id: int) -> set[int]:
    session = Database().create_session()
    query = session.query(Blacklist)
    records = query.all()
    res = []
    [
        res.append(int(blacklist.blocked_vk_user_id))
        for blacklist in records
        if blacklist.user_id == user_id
    ]
    session.close()
    return set(res)


def get_user_favorites(user_id: int) -> set[int]:
    session = Database().create_session()
    query = session.query(Favorite)
    records = query.all()
    res = []
    [
        res.append(int(favorite.favorite_vk_user_id))
        for favorite in records
        if favorite.user_id == user_id
    ]
    session.close()
    return set(res)


# Проверяет существует ли юзер
def check_user_exits(user_id: int) -> bool:
    Database().check_database(Database().create_connect())
    session = Database().create_session()
    query = session.query(User).filter(User.user_id == user_id).first()
    if query is None:
        result = False
    else:
        result = True
    session.close()
    return result


# Добавляет данные в базу
def set_user_data(user_id: int, param_dict: dict):
    session = Database().create_session()
    query = session.query(User).filter(User.user_id == user_id).first()
    if query != None:
        if param_dict.get("gender") != None:
            query.search_gender = param_dict.get("gender")
        elif param_dict.get("city") != None:
            query.search_city = param_dict.get("city")
        elif param_dict.get("age_min") != None:
            query.search_age_min = param_dict.get("age_min")
        elif param_dict.get("age_max") != None:
            query.search_age_max = param_dict.get("age_max")
        elif param_dict.get("user_name") != None:
            query.user_name = param_dict.get("user_name")
        elif param_dict.get("state") != None:
            query.state = param_dict.get("state")
        res = "{} {} {}".format("Данные пользователя с id:", user_id, "обновлены")
    else:
        res = "{} {} {}".format("Пользователь с id:", user_id, "не существует в БД")
    session.commit()
    session.close()
    return res


# пола и города может не быть
def create_user_and_set_data(param_dict: dict):
    # dict_example3 = {"user_id": 123, "gender": 0, "city": "Moscow"}
    session = Database().create_session()
    if not check_user_exits(param_dict.get("user_id")):
        user = User(
            user_id=param_dict.get("user_id"),
            user_name=param_dict.get("user_name"),
            search_gender=param_dict.get("gender"),
            search_age_min=param_dict.get("age_min"),
            search_age_max=param_dict.get("age_max"),
            search_city=param_dict.get("city"),
            state=param_dict.get("state"),
        )
        session.add(user)
        session.commit()
        if check_user_exits(param_dict.get("user_id")):
            res = "{} {} {}".format(
                "Пользователь с id:", param_dict.get("user_id"), "добавлен в БД"
            )
    else:
        res = "{} {} {}".format(
            "Пользователь с id:", param_dict.get("user_id"), "уже есть в БД"
        )
    session.close()
    return res


# Для теста запросов к БД
def read_json(file_name):
    session = Database().create_session()

    with open(file_name, "r", encoding="utf-8") as f:
        data = json.load(f)
        for record in data:
            if record.get("model") == "user":
                model = {"user": User, "blacklist": Blacklist, "favorite": Favorite}[
                    record.get("model")
                ]
                session.add(model(user_id=record.get("pk"), **record.get("fields")))
            if record.get("model") == "blacklist":
                model = {"user": User, "blacklist": Blacklist, "favorite": Favorite}[
                    record.get("model")
                ]
                session.add(
                    model(blacklist_id=record.get("pk"), **record.get("fields"))
                )
            if record.get("model") == "favorite":
                model = {"user": User, "blacklist": Blacklist, "favorite": Favorite}[
                    record.get("model")
                ]
                session.add(model(favorite_id=record.get("pk"), **record.get("fields")))
        session.commit()
    session.close()


def set_blacklist_user(client_user_id: int, blacklist_user_id: int):
    session = Database().create_session()
    if check_user_exits(client_user_id):
        query = (
            session.query(Blacklist).join(User).filter(User.user_id == client_user_id).all()
        )
        res = []
        [
            res.append(blacklist.blocked_vk_user_id)
            for blacklist in query
            if blacklist.user_id == client_user_id
        ]

        if blacklist_user_id not in res:
            user = Blacklist(user_id=client_user_id, blocked_vk_user_id=blacklist_user_id)
            res.append(blacklist_user_id)
            session.add(user)
            session.commit()
        session.close()
        return res


def set_favourite_user(client_user_id: int, favourite_user_id: int):
    session = Database().create_session()
    if check_user_exits(client_user_id):
        query = (
            session.query(Favorite).join(User).filter(User.user_id == client_user_id).all()
        )
        res = []
        [
            res.append(favorite.favorite_vk_user_id)
            for favorite in query
            if favorite.user_id == client_user_id
        ]
        if favourite_user_id not in res:
            user = Favorite(user_id=client_user_id, favorite_vk_user_id=favourite_user_id)
            res.append(favourite_user_id)
            session.add(user)
            session.commit()
        session.close()
        return res

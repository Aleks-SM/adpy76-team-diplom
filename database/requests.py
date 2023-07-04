import json
from sqlalchemy.orm import sessionmaker
from database.models import User, Favorite, Blacklist
from database.database import Database
from database.db_dataclassess import ClientUser


#Должна возращать ClientUser, если данных нет, то пустые поля должны быть None
def get_user_data(user_id: int) -> ClientUser:
    Session = sessionmaker(bind=Database().create_conect())
    session = Session()

    for query in session.query(User).filter(User.user_id == user_id).all():
        self = ClientUser(user_id=query.user_id,
                   age_min=query.search_age_min,
                   age_max=query.search_age_max,
                   gender=query.search_gender,
                   city=query.search_city,
                   state=query.state)
    return self


# Должна возвращать сет из blocked_vk_user_id
def get_user_blacklist(user_id: int) -> set[int]:
    Session = sessionmaker(bind=Database().create_conect())
    session = Session()
    # query = session.query(User, Blacklist)
    # query = session.join(UserBlacklist, UserBlacklist.user_id == User.user_id)
    # records = query.all()
    # for user, blacklist in records:
        
    for query in session.query(User, Blacklist).join(UserBlacklist).filter(UserBlacklist.user_id == User.user_id).all():
        query_result = {"user_id": query.user_id,
                       "blocked_vk_id": query.blocked_vk_user_id}
    return query_result


# Проверяет существует ли юзер
def check_user_exits(user_id: int) -> bool:
    pass


# Добавляет данные в базу
def set_user_data(user_id: int, param_dict: dict):
    dict_example = {"age_min": 23}
    dict_example2 = {"city": "Moscow"}


# пола и города может не быть
def create_user_and_set_data(param_dict: dict):
    dict_example3 = {"user_id": 123,
                     "gender": 0,
                     "city": "Moscow"}

# Для теста запросов к БД
def read_json(file_name):
    Session = sessionmaker(bind=Database().create_conect())
    session = Session()

    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for record in data:
            model = {
                'user': User,
                'blacklist': Blacklist,
                'favorite': Favorite,
            }[record.get('model')]
            session.add(model(user_id=record.get('pk'), **record.get('fields')))
        session.commit()
    session.close()

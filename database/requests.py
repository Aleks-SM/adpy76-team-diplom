from database.db_dataclassess import ClientUser
from sqlalchemy.orm import sessionmaker
from database.models import User, Favorite, Blacklist
from database.database import Database
from database.db_dataclassess import ClientUser


#Должна возращать ClientUser
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
def get_user_blacklist() -> set[int]:
    Session = sessionmaker(bind=Database().create_conect())
    session = Session()
    for query in session.query(User).join(Blacklist).filter(User.user_id == user_id).all():
        query_result = {"user_id": query.user_id,
                       "blocked_vk_id": query.blocked_vk_user_id}
    return query_result


#Проверяет существует ли юзер
def check_user_exits(user_id: int) -> bool:
    pass

from database.db_dataclassess import ClientUser
from sqlalchemy.orm import sessionmaker
from database.models import User, Favorite, Blacklist
def get_user_data(engine, user_id: int) -> ClientUser:
    Session = sessionmaker(bind=engine)
    session = Session()

    for query in session.query(User).filter(User.user_id == user_id).all():
        query_result = {'user_id': query.user_id,
                        'age_first': query.search_age.split('-')[0],
                        'age_last': query.search_age.split('-')[1],
                        'gender': query.search_gender,
                        'city': query.search_city,
                        'state': query.state}
        query_result1 = {'user_id': query.user_id,
                        'age':[query.search_age.split('-')[0], query.search_age.split('-')[1]],
                        'gender': query.search_gender,
                        'city': query.search_city,
                        'state': query.state}
        # 'state': query.query}
        # print(
        #     "{} {}\n{} {}\n{} {}\n{} {}\n{} {}".format(
        #         "user id:", query.user_id,
        #         "username:", query.user_name,
        #         "search gender:", query.search_gender,
        #         "search age:", query.search_age,
        #         "search city:", query.search_city,
        #     )
        # )
    return print(query_result, query_result1, sep='\n')

def check_user_exits(user_id: int) -> bool:
    pass

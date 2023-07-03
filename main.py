from database.database import Database
from database.requests import get_user_data

if __name__ == "__main__":
    base = Database()
    # base.create_tables(base.create_conect())
    print(get_user_data(1))

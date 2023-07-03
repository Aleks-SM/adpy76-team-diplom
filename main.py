import os
from database.database import Database
from database.requests import get_user_data, read_json

if __name__ == "__main__":
    base = Database()
    base.create_tables(base.create_conect())
    read_json(base.filename)
    print(get_user_data(1))

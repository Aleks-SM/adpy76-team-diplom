from database.database import Database
from database.requests import get_user_data

if __name__ == "__main__":
    base = Database()
    # base.create_tables(sq.create_engine(base.create_conect()))
    get_user_data(1)

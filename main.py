import sqlalchemy as sq
from database.database import Database

if __name__ == "__main__":
    base = Database()
    base.create_tables(sq.create_engine(base.create_conect()))

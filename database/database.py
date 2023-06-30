import os
from dotenv import load_dotenv
from database.models import Base


class Database:
    def __init__(self):
        if os.path.join(os.path.dirname(__file__), ".envrc"):
            path = os.path.split(os.path.dirname(__file__))
            dotenv_path = os.path.join(path[0], ".envrc")
        else:
            dotenv_path = os.path.join(os.path.dirname(__file__), ".envrc")
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        self.bd = os.getenv("bd")
        self.bd_port = os.getenv("bd_port")
        self.bd_name = os.getenv("bd_name")
        self.bd_username = os.getenv("bd_username")
        self.bd_pass = os.getenv("bd_pass")
        self.bd_host = os.getenv("bd_host")
        self.token = os.getenv("token")

    def create_conect(self):
        dsn = "{}://{}:{}@{}:{}/{}".format(
            self.bd,
            self.bd_username,
            self.bd_pass,
            self.bd_host,
            self.bd_port,
            self.bd_name,
        )
        return dsn

    def create_tables(self, engine):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

from database.database import Database
from vk_api.listener import bot

if __name__ == "__main__":
    base = Database()
    base.create_tables(base.create_connect())
    bot.run_forever()
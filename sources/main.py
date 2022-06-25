import peewee
import aiogram
from models.User import User
from models.List import List
from models.Item import Item
from models.db import database


def main():
    u = User(telegram_id=123)
    u.save()
    pass


if __name__ == "__main__":
    main()

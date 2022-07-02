import peewee

from db.models.Base import Base
from db.models.List import List
from db.db import database, create_tables


__all__ = [
    "User",
]


class User(Base):
    class Meta:
        db_table = 'users'

    telegram_id = peewee.BigIntegerField(null=False, unique=True)
    current_list_id = peewee.ForeignKeyField(List, field='id', backref='current-list', null=True)
    language = peewee.TextField(default='en')


create_tables(database, [User])

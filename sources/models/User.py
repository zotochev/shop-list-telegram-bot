import peewee

from sources.models.Base import Base
from sources.models.List import List


__all__ = [
    "User",
]


class User(Base):
    class Meta:
        db_table = 'users'

    telegram_id = peewee.BigIntegerField()
    current_list_id = peewee.ForeignKeyField(List, field='id', backref='current-list')
    language = peewee.TextField()

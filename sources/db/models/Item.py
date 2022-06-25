import peewee
from sources.db.models.Base import Base
from sources.db.models.List import List
from sources.db.db import database, create_tables


__all__ = [
    "Item",
]


class Item(Base):
    class Meta:
        db_table = 'items'

    list_id = peewee.ForeignKeyField(List, backref='from-list', field='id')
    creation_time = peewee.DateTimeField()
    is_done = peewee.BooleanField()
    data = peewee.TextField()


create_tables(database, [Item])

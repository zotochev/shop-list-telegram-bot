import peewee
from Base import Base
from List import List


__all__ = [
    "Item",
]


class Item(Base):
    class Meta:
        db_table = 'items'

    list_id = peewee.ForeignKeyField(List, backref='from-list')
    creation_time = peewee.DateTimeField()
    is_done = peewee.BooleanField()
    data = peewee.TextField()

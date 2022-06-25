import peewee
from sources.models.Base import Base
from sources.models.db import database, create_tables


__all__ = [
    "List",
]


class List(Base):
    class Meta:
        db_table = 'lists'

    name = peewee.TextField(null=False)
    user_id = peewee.DeferredForeignKey('User', backref='whose-list', field='id')
    is_deleted = peewee.BooleanField(default=False)
    is_done = peewee.BooleanField(default=False)
    schema = peewee.TextField(null=True)


create_tables(database, [List])

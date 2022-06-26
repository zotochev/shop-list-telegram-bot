import peewee
from sources.db.models.Base import Base
from sources.db.models.Record import Record
from sources.db.db import database, create_tables


__all__ = [
    "List",
]


class List(Base):
    class Meta:
        db_table = 'lists'

    name = peewee.TextField(null=False)
    user_id = peewee.DeferredForeignKey('User', backref='whose-list', field='id')
    current_record = peewee.ForeignKeyField(Record, backref='current-record', field='id', null=True)
    is_deleted = peewee.BooleanField(default=False)
    is_done = peewee.BooleanField(default=False)
    schema = peewee.TextField(null=True)


create_tables(database, [List])

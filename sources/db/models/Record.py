import peewee
from sources.db.models.Base import Base
# from sources.db.models.List import List
from sources.db.db import database, create_tables


__all__ = [
    "Record",
]


class Record(Base):
    class Meta:
        db_table = 'records'

    list_id = peewee.DeferredForeignKey('List', backref='from-list', field='id', null=True)
    creation_time = peewee.TimestampField()
    is_done = peewee.BooleanField(default=False)
    is_delete = peewee.BooleanField(default=False)
    data = peewee.TextField()


create_tables(database, [Record])

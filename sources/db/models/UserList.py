import peewee
from db.models.Base import Base
from db.models.Record import Record
from db.db import database, create_tables


__all__ = [
    "UserList",
]


class UserList(Base):
    class Meta:
        db_table = 'user_list'

    user_id = peewee.DeferredForeignKey('User', backref='whose-list', field='id')
    list_id = peewee.DeferredForeignKey('List', backref='whose-user', field='id')


create_tables(database, [UserList])

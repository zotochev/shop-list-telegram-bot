import peewee
from Base import Base
from User import User


__all__ = [
    "List",
]


class List(Base):
    class Meta:
        db_table = 'lists'

    name = peewee.TextField(null=False)
    user_id = peewee.ForeignKeyField(User, backref='whose-list')
    is_deleted = peewee.BooleanField(default=False)
    is_done = peewee.BooleanField(default=False)
    schema = peewee.TextField(null=True)

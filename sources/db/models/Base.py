import peewee
from sources.db.db import database


__all__ = [
    "Base"
]


class Base(peewee.Model):
    class Meta:
        database = database

    created = peewee.TimestampField()

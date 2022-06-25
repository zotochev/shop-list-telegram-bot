import peewee
from sources.models.db import database


__all__ = [
    "Base"
]


class Base(peewee.Model):
    class Meta:
        database = database

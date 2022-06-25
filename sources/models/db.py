import peewee


__all__ = [
    "database",
]


database = peewee.SqliteDatabase('shop-list.db')

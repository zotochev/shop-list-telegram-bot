import peewee


__all__ = [
    "database",
]


database = peewee.SqliteDatabase('shop-list.db')


def create_tables(db: peewee.SqliteDatabase, tables: list[peewee.Model]):
    with db:
        db.create_tables(tables)

import peewee
from pathlib import Path


__all__ = [
    "database",
]


database = peewee.SqliteDatabase(Path(Path(__file__).parent, 'shop-list.db'))


def create_tables(db: peewee.SqliteDatabase, tables: list[peewee.Model]):
    with db:
        db.create_tables(tables)

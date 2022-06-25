import pydantic
from pydantic import BaseModel


class Base(BaseModel):
    id: int



class Item(BaseModel):
    id: int
    list_id: int
    creation_time: int
    is_done: bool
    data: dict


class List(BaseModel):
    id: int
    name: str
    user_id: int
    is_deleted: bool
    schema: dict


class User(BaseModel):
    telegram_id: int
    current_list_id: int
    language: str


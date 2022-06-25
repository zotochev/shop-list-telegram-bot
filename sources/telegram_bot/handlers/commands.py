import os
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from sources.telegram_bot.bot_init import bot
from sources.db.models import User
from sources.db.models import List
from sources.db.models import Item


# @dp.message_handler(commands=['start'])
async def send_start(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    users = User.select().where(User.telegram_id == telegram_id)
    if not users:
        new_user = User.create(telegram_id=telegram_id, language=message.from_user.language_code)
        new_user.save()
        new_list = List.create(name='default',
                               user_id=new_user.id,
                               )
        new_list.save()

        query = User.update(current_list_id=new_list.id).where(User.id == new_user.id)
        query.execute()
        await message.answer("You successfully registered!")

    await message.answer("Hello!")


# @dp.message_handler(commands=['help'])
async def send_help(message: types.Message, state: FSMContext):
    await message.answer(message.text)


async def send_test(message: types.Message, state: FSMContext):

    await message.answer("This is test!")


async def send_list(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = User.select().where(User.telegram_id == telegram_id).get()
    # print(user)
    current_list = List.select().where(List.id == user.current_list_id).get()
    items = Item.select().where(Item.list_id == current_list.id)
    if not items:
        await message.answer('You have no records.')


def is_registered(message: types.Message) -> bool:
    return bool(User.select().where(User.telegram_id == message.from_user.id))


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(send_start, commands=['start'], state='*')
    dp.register_message_handler(send_help, commands=['help'], state='*')

    dp.register_message_handler(send_list, is_registered, commands=['list'], state='*')
    dp.register_message_handler(send_test, is_registered, commands=['test'], state='*')

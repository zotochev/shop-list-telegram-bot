import typing

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from db.models import User
from db.models import List
from db.models import Record

from telegram_bot.config import Reactions, ADMINS, prepare_for_md


# @dp.message_handler(commands=['start'])
async def send_start(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    users = User.select().where(User.telegram_id == telegram_id)
    if not users:
        new_user = User.create(telegram_id=telegram_id, language=message.from_user.language_code)
        new_user.save()
        new_list = List.create(name='default',
                               user_id=new_user.id)
        new_list.save()

        query = User.update(current_list_id=new_list.id).where(User.id == new_user.id)
        query.execute()
        await message.answer(Reactions(message).registered(), parse_mode='MarkdownV2')

    await message.answer(Reactions(message).start(), parse_mode='MarkdownV2')


# @dp.message_handler(commands=['help'])
async def send_help(message: types.Message, state: FSMContext):
    await message.answer(Reactions(message).help(), parse_mode='MarkdownV2')


def get_current_list(telegram_id: int) -> dict:
    """
    Returns:
        {
            "name": "list_name",
            "list_id": 2,
            "records": [record(id: 1, data: "foobar", is_done: False), ...],
            "current_record_id": 2
        }
    """

    user = User.select().where(User.telegram_id == telegram_id).get()
    current_list = List.select().where(List.id == user.current_list_id).get()
    if current_list.current_record:
        current_record_id = current_list.current_record.id
    else:
        current_record_id = -1
    records = Record.select().where(Record.list_id == current_list.id)

    result = {'name': current_list.name,
              'list_id': current_list.id,
              'records': [],
              'current_record_id': current_record_id}
    if records:
        result['records'] = [x for x in records if not x.is_delete]
    return result


def get_list_by_name(telegram_id: int, list_name: str) -> typing.Optional[dict]:
    """
    Returns:
        {
            "name": "list_name",
            "list_id": 2,
            "records": [record(id: 1, data: "foobar", is_done: False), ...],
            "current_record_id": 2
        }
    """

    user = User.select().where(User.telegram_id == telegram_id).get()
    found_list = List.select().where((List.user_id == user.id) & (List.name == list_name))
    result = None

    if found_list:
        found_list = found_list.get()
        records = Record.select().where(Record.list_id == found_list.id)
        result = {'name': found_list.name,
                  'list_id': found_list.id,
                  'records': [x for x in records if not x.is_delete],
                  'current_record_id': found_list.current_record.id if found_list.current_record else None}
    return result


def prepare_list_to_send(records: dict) -> typing.Optional[str]:
    current_record_id = records['current_record_id']

    if not records['records']:
        return None
    else:
        result = []
        for i, x in enumerate(records['records']):
            record_temp = prepare_for_md(x.data)
            if x.id == current_record_id:
                record_temp = f"__{record_temp}__"
            if x.is_done:
                record_temp = f"~{record_temp}~"
            if not x.is_delete:
                result.append(f"{i + 1: 2}\. {record_temp}")

        to_send = f"*{prepare_for_md(records['name'])}*:\n" + "\n".join(result)
        return to_send


async def send_list(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    records = get_current_list(telegram_id=telegram_id)
    answer = prepare_list_to_send(records)
    if not answer:
        answer = Reactions(message).no_records()
    await message.answer(answer, parse_mode='MarkdownV2')


async def send_lists(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = User.select().where(User.telegram_id == telegram_id).get()
    current_list_id = user.current_list_id.id if user.current_list_id else -1
    lists = List.select().where((List.user_id == user.id) & (List.is_deleted == False))

    answer = "\n".join([f"/\_{prepare_for_md(x.name)}" if x.id != current_list_id else f"/\___{prepare_for_md(x.name)}__"
                        for x in lists])
    await message.answer(answer, parse_mode='MarkdownV2')


async def change_list(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    user = User.select().where(User.telegram_id == telegram_id).get()
    new_list_name = message.text[6:] if message.text.startswith('/list') else message.text[2:]
    records = get_list_by_name(telegram_id, new_list_name)

    if not records:
        new_list = List.create(name=new_list_name,
                               user_id=user.id)
        new_list.save()
        query = User.update(current_list_id=new_list.id).where(User.id == user.id)
        query.execute()
        await message.answer(Reactions(message).new_list(new_list_name), parse_mode='MarkdownV2')
    else:
        query = User.update(current_list_id=records['list_id']).where(User.id == user.id)
        query.execute()
        answer = prepare_list_to_send(records)
        if not answer:
            answer = Reactions(message).no_records()
        await message.answer(answer, parse_mode='MarkdownV2')


async def add_record(message: types.Message, state: FSMContext):
    user = User.select().where(User.telegram_id == message.from_user.id).get()
    current_list = List.select().where(List.id == user.current_list_id).get()
    record = Record.create(list_id=current_list.id, data=message.text)
    record.save()

    query = List.update(current_record=record.id).where(List.id == current_list.id)
    query.execute()

    records = get_current_list(telegram_id=message.from_user.id)
    answer = prepare_list_to_send(records)
    if not answer:
        answer = Reactions(message).no_records()
    await message.delete()
    await message.answer(answer, parse_mode='MarkdownV2')


async def change_current_record(message: types.Message, state: FSMContext):
    direction = get_direction(message.text)
    if not direction:
        raise Exception(f'Wrong message text {message.text}\.')

    user = User.select().where(User.telegram_id == message.from_user.id).get()
    current_list = List.select().where(List.id == user.current_list_id).get()
    records = Record.select().where((Record.list_id == current_list.id) & (Record.is_delete == False))
    current_record_id = current_list.current_record.id if current_list.current_record else None
    records_ids = [x.id for x in records]
    if records_ids:
        index = records_ids.index(current_record_id)

        new_current_record_id = records_ids[(index + direction) % len(records_ids)]

        query = List.update(current_record=new_current_record_id).where(List.id == current_list.id)
        query.execute()

        records = get_current_list(telegram_id=message.from_user.id)
        answer = prepare_list_to_send(records)
        if not answer:
            answer = Reactions(message).no_records()
        # await message.delete()
        await message.answer(answer, parse_mode='MarkdownV2')


async def done_record(message: types.Message, state: FSMContext):

    user = User.select().where(User.telegram_id == message.from_user.id).get()
    current_list = List.select().where(List.id == user.current_list_id).get()
    current_record_id = current_list.current_record.id if current_list.current_record else None
    records = Record.select().where((Record.list_id == current_list.id) & (Record.is_delete == False))
    # records_ids = [x.id for x in records]

    # if records_ids:
    #     index = records_ids.index(current_record_id)
    #     if index == len(records_ids) - 1:
    #         direction = -1
    #     else:
    #         direction = 1
    #     new_current_record_id = records_ids[(index + direction) % len(records_ids)]
    #     query = List.update(current_record=new_current_record_id).where(List.id == current_list.id)
    #     query.execute()

    if current_record_id:
        current_record = Record.select().where(Record.id == current_record_id).get()
        current_done_status = current_record.is_done
        query = Record.update(is_done=not current_done_status).where(Record.id == current_record_id)
        query.execute()

    records = get_current_list(telegram_id=message.from_user.id)
    answer = prepare_list_to_send(records)
    if not answer:
        answer = Reactions(message).no_records()
    # await message.delete()
    await message.answer(answer, parse_mode='MarkdownV2')


async def delete_record(message: types.Message, state: FSMContext):

    user = User.select().where(User.telegram_id == message.from_user.id).get()
    current_list = List.select().where(List.id == user.current_list_id).get()
    current_record_id = current_list.current_record.id if current_list.current_record else None

    records = Record.select().where((Record.list_id == current_list.id) & (Record.is_delete == False))
    records_ids = [x.id for x in records]

    if records_ids:
        index = records_ids.index(current_record_id)
        if index == len(records_ids) - 1:
            direction = -1
        else:
            direction = 1
        new_current_record_id = records_ids[(index + direction) % len(records_ids)]
        query = List.update(current_record=new_current_record_id).where(List.id == current_list.id)
        query.execute()

    if current_record_id:
        query = Record.update(is_delete=True).where(Record.id == current_record_id)
        query.execute()

    records = get_current_list(telegram_id=message.from_user.id)
    answer = prepare_list_to_send(records)
    if not answer:
        answer = Reactions(message).no_records()
    # await message.delete()
    await message.answer(answer, parse_mode='MarkdownV2')


async def get_users(message: types.Message):
    if ADMINS:
        admins_id = []

        admins = ADMINS.split()
        for admin in admins:
            try:
                telegram_id = int(admin)
                admins_id.append(telegram_id)
            except Exception as e:
                pass
        if message.from_user.id in admins_id:
            list_users = User.select()
            if list_users:
                answer = "\n".join([f"{x.telegram_id} - {x.language}" for x in list_users])
                await message.answer(answer)
            else:
                await message.answer('No users.')


def is_registered(message: types.Message) -> bool:
    return bool(User.select().where(User.telegram_id == message.from_user.id))


def short_change_list(message: types.Message) -> bool:
    return (message.text.startswith('/_')
            and message.text[2:3] != ' '
            and len(message.text) > 3)


def get_direction(m: str) -> int:
    if m == '/^' or m == '/A' or m == '/a' or m == '/up' or m == '/UP':
        return -1
    elif m == '/v' or m == '/V' or m == '/d' or m == '/down' or m == '/DOWN':
        return 1
    else:
        return 0


def is_change_current_record(message: types.Message) -> bool:
    m = message.text
    return bool(get_direction(m))


def register_handlers_commands(dp: Dispatcher):
    dp.register_message_handler(send_start, commands=['start'], state='*', content_types=types.ContentType.TEXT)
    dp.register_message_handler(send_help, commands=['help'], state='*', content_types=types.ContentType.TEXT)
    dp.register_message_handler(get_users, commands=['users'], state='*', content_types=types.ContentType.TEXT)

    dp.register_message_handler(send_list, is_registered, lambda m: len(m.text) == 5, commands=['list'], state='*', content_types=types.ContentType.TEXT)
    dp.register_message_handler(send_list, is_registered, lambda m: m.text == '/', state='*', content_types=types.ContentType.TEXT)
    dp.register_message_handler(change_list, is_registered, lambda m: len(m.text) > 5, commands=['list'], state='*', content_types=types.ContentType.TEXT)
    dp.register_message_handler(change_list, is_registered, short_change_list, state='*', content_types=types.ContentType.TEXT)
    dp.register_message_handler(send_lists, is_registered, commands=['lists'], state='*', content_types=types.ContentType.TEXT)

    dp.register_message_handler(change_current_record, is_registered, commands=[
        '^', 'a', 'A', 'up', 'UP',
        'v', 'V', 'd', 'down', 'DOWN'
    ], state='*', content_types=types.ContentType.TEXT)

    dp.register_message_handler(done_record, is_registered, commands=['done', 'x', 'X'], state='*', content_types=types.ContentType.TEXT)
    dp.register_message_handler(delete_record, is_registered, commands=['del', 'delete'], state='*', content_types=types.ContentType.TEXT)

    dp.register_message_handler(add_record, is_registered, lambda m: True, state='*', content_types=types.ContentType.TEXT)

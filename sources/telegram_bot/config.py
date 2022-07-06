import os
from aiogram import types, Dispatcher

from telegram_bot.bot_exceptions import BotInitException


WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
if WEBHOOK_HOST is None or WEBHOOK_PATH is None:
    raise BotInitException(f'WEBAPP HOST: {WEBHOOK_HOST}, PATH: {WEBHOOK_PATH}')

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = os.getenv('WEBAPP_PORT')
if WEBAPP_HOST is None or WEBAPP_PORT is None:
    raise BotInitException(f'WEBAPP HOST: {WEBAPP_HOST}, PORT: {WEBAPP_PORT}')

TOKEN = os.environ.get('TELEGRAM_TOKEN')
if TOKEN is None:
    raise BotInitException('TOKEN_NOT_FOUND')

ADMINS = os.getenv('ADMINS', None)


def prepare_for_md(text: str) -> str:
    for c in "_*[]()~`>#+-=|{}.!":
        text = text.replace(c, '\\' + c)
    return text


REACTIONS = {
    'en': {
        'help': ("After sending /start command you automatically "
                 "registered in the bot system.\n"
                 "\n"
                 "On the start you have the default list with no records. "
                 "To add a record send any text message to the bot.\n"
                 "\n"
                 "*Supported commands*:\n"
                 "/list or just / - to see all records of the current list.\n"
                 "/list list_name or /_list_name - to change current list or create new one.\n"
                 "/lists - to see all your lists.\n"
                 "\n"
                 "*Navigation*:\n"
                 '/^, /a, /A, /up, /UP - to set previous record as current.\n'
                 '/v, /V, /d, /down, /DOWN - to set next record as current.\n'
                 "\n"
                 "*Change record status*:\n"
                 "/x, /X, /done - to set current record as done.\n"
                 "/del, /delete - to delete current record.\n"
                 ),
        'start': ("Hello! I am the *Shop List* bot. You can create and manage simple "
                  "lists of any purpose with me. Send /help for more information."),
        'registered': 'You successfully registered!',
        'new_list': '{} created.',
        'no_records': 'List has no records.',
    }
}


class Reactions:
    def __init__(self, message: types.Message):
        self.language_code = message.from_user.language_code

    def _get_reaction(self, reaction: str):
        language = self.language_code if REACTIONS.get(self.language_code) else 'en'
#         return prepare_for_md(REACTIONS[language].get(reaction, 'Unknown reaction.'))
        return REACTIONS[language].get(reaction, 'Unknown reaction.')

    
    def start(self):
        return self._get_reaction('start')

    def help(self):
        return self._get_reaction('help')

    def registered(self):
        return self._get_reaction('registered')

    def no_records(self):
        return self._get_reaction('no_records')

    def new_list(self, list_name: str):
        return self._get_reaction('new_list').format(list_name)

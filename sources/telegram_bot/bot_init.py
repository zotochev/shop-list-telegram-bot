from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

from sources.telegram_bot.bot_exceptions import BotInitException


TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    raise BotInitException('TOKEN_NOT_FOUND')

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

from sources.telegram_bot.bot_exceptions import BotInitException
from sources.main import WEBHOOK_URL


TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    raise BotInitException('TOKEN_NOT_FOUND')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

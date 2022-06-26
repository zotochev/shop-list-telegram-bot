from aiogram import Bot, Dispatcher
# from aiogram.contrib.fsm_storage.memory import MemoryStorage

from sources.telegram_bot.config import WEBHOOK_URL, TOKEN


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # insert code here to run it after start


async def on_shutdown(dp):
    # Remove webhook (not acceptable in some cases)
    # await bot.delete_webhook()

    # Close DB connection (if used)
    # await dp.storage.close()
    # await dp.storage.wait_closed()
    pass

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
# storage = MemoryStorage()
dp = Dispatcher(bot)

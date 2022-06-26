import os
from aiogram import executor

from telegram_bot.bot_init import dp
from telegram_bot.handlers import commands
from telegram_bot.bot_init import on_startup, on_shutdown


# webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# WEBAPP_HOST = 'localhost'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT')


def main():
    commands.register_handlers_commands(dp)
    executor.start_webhook(
                           dispatcher=dp,
                           webhook_path=WEBHOOK_PATH,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown,
                           host=WEBAPP_HOST,
                           port=WEBAPP_PORT
    )
    # http://0.0.0.0:8080
    # executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()

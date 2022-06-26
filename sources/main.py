import os
from aiogram import executor

from telegram_bot.bot_init import dp
from telegram_bot.handlers import commands


# webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


def main():
    commands.register_handlers_commands(dp)
    executor.start_webhook(
                           dispatcher=dp,
                           webhook_path=WEBHOOK_PATH,
                           skip_updates=True,
    )
    # executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
